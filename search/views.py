from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query

def search(request):
    search_query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    if search_query:
        # 这一行代码会根据所有模型的 search_fields 自动穿透检索
        search_results = Page.objects.live().search(search_query)
        
        # 记录用户的搜索词（用于后台统计，可选）
        Query.get(search_query).add_hit()
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