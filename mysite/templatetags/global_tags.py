from django import template
from wagtail.models import Site

register = template.Library()

@register.simple_tag
def get_footer_text():
    return "我们是一个致力于传播新闻与信息的机构，提供最新动态与关键报道。"

@register.simple_tag(takes_context=True)
def get_footer_navigation(context):
    request = context.get("request")
    site = None

    if request is not None:
        site = Site.find_for_request(request)

    if site is None:
        site = Site.find_for_default_site()

    if site is None:
        return []

    return site.root_page.get_children().live()
