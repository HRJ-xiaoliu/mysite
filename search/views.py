from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.db.models import Q, CharField, TextField
from django.apps import apps
from wagtail.models import Page, get_page_models
from wagtail.fields import RichTextField, StreamField
from wagtail.contrib.search_promotions.models import Query
from modelcluster.fields import ParentalKey

def search(request):
    search_query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    result_list = []

    if search_query:
        for model in get_page_models():
            if model is Page:
                continue
            
            q_objects = Q(title__icontains=search_query) | Q(search_description__icontains=search_query)
            for field in model._meta.get_fields():
                if isinstance(field, (CharField, TextField, RichTextField, StreamField)):
                    if field.name not in ['path', 'depth', 'numchild', 'url_path', 'translation_key', 'content_type']:
                        q_objects |= Q(**{f"{field.name}__icontains": search_query})
            
            hits = model.objects.live().filter(q_objects)
            for hit in hits:
                snippet = getattr(hit, 'intro', getattr(hit, 'search_description', ''))
                if not snippet and hasattr(hit, 'body'):
                    snippet = str(hit.body)[:200]

                result_list.append({
                    'title': hit.title,
                    'url': hit.get_url(),
                    'type_label': getattr(model._meta, 'verbose_name', hit.content_type.name),
                    'snippet': snippet,
                    'date': hit.first_published_at,
                    'source': hit.owner.get_full_name() if hit.owner else '全站节点'
                })

        for model in apps.get_models():
            parental_keys = [
                f for f in model._meta.get_fields() 
                if isinstance(f, ParentalKey) and issubclass(f.related_model, Page)
            ]
            
            if parental_keys:
                q_objects = Q()
                for field in model._meta.get_fields():
                    if isinstance(field, (CharField, TextField, RichTextField, StreamField)):
                        q_objects |= Q(**{f"{field.name}__icontains": search_query})
                
                if q_objects:
                    child_hits = model.objects.filter(q_objects)
                    for hit in child_hits:
                        parent_page = None
                        for pk_field in parental_keys:
                            parent_obj = getattr(hit, pk_field.name)
                            if parent_obj:
                                parent_page = parent_obj.specific
                                break
                        
                        if parent_page and parent_page.live:
                            type_name = getattr(model._meta, 'verbose_name', model.__name__)
                            if hasattr(hit, 'get_pub_type_display'):
                                type_name = hit.get_pub_type_display()
                            elif hasattr(hit, 'role'):
                                type_name = '科研项目'

                            title = getattr(hit, 'title', f"附属条目：{parent_page.title}")
                            snippet = getattr(hit, 'abstract', getattr(hit, 'description', ''))
                            source_info = getattr(hit, 'authors', getattr(hit, 'venue', parent_page.title))

                            result_list.append({
                                'title': title,
                                'url': parent_page.get_url(),
                                'type_label': type_name,
                                'snippet': snippet,
                                'date': parent_page.first_published_at,
                                'source': source_info
                            })

        unique_results = []
        seen = set()
        for r in result_list:
            identifier = f"{r['title']}-{r['url']}"
            if identifier not in seen:
                seen.add(identifier)
                unique_results.append(r)
        
        def get_sort_key(item):
            return str(item['date']) if item['date'] else "0000"
        
        unique_results.sort(key=get_sort_key, reverse=True)
        result_list = unique_results

        if search_query.strip():
            Query.get(search_query).add_hit()
    
    paginator = Paginator(result_list, 10)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': page_obj,
        'paginator': paginator,
    })