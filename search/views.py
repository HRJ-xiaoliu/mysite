from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.db.models import Q
from wagtail.models import Page
from blog.models import BlogPage 

def search(request):
    search_query = request.GET.get('q', None)
    page = request.GET.get('page', 1)

    if search_query:
        base_page_ids = list(Page.objects.live().filter(
            Q(title__icontains=search_query) |
            Q(search_description__icontains=search_query)
        ).values_list('id', flat=True))

        blog_page_ids = list(BlogPage.objects.live().filter(
            Q(intro__icontains=search_query) |
            Q(body__icontains=search_query)
        ).values_list('id', flat=True))

        hit_ids = set(base_page_ids + blog_page_ids)

        search_results = Page.objects.live().filter(id__in=hit_ids).order_by('-first_published_at')

    else:
        search_results = Page.objects.none()

    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })