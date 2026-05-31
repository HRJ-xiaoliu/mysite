from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField

# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from .blocks import HomeStreamBlock

# 引入搜索引模块
from wagtail.search import index
from django.utils.html import strip_tags
from wagtail.blocks import StreamValue
from django.db.models.manager import Manager

class GlobalSearchMixin(Page):
    class Meta:
        abstract = True 

    @property
    def auto_search_text(self):
        texts = []
        possible_fields = ['intro', 'body', 'description', 'content', 'biography', 'hero_text', 'about_us', 'authors', 'tags']
        
        for field in possible_fields:
            if hasattr(self, field):
                value = getattr(self, field)
                
                if not value:
                    continue
                    
                if isinstance(value, StreamValue):
                    for block in value:
                        searchable_content = block.block.get_searchable_content(block.value)
                        if searchable_content:
                            texts.extend([strip_tags(str(item)) for item in searchable_content])
                
                elif isinstance(value, Manager) or hasattr(value, 'all'):
                    for related_obj in value.all():
                        texts.append(strip_tags(str(related_obj)))
                        
                else:
                    texts.append(strip_tags(str(value)))
                    
        return " ".join(texts)

    search_fields = Page.search_fields + [
        index.SearchField('auto_search_text'),
    ]
    
class HomePage(Page):
    # add the Hero section of HomePage:
    header_background = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="全局头部背景图"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    hero_text = models.CharField(
        blank=True,
        max_length=255, help_text="Write an introduction for the site"

    )
    
    # 核心修改：明确指定 use_json_field=True，解决底层字符串解析报错
    body = StreamField(
        HomeStreamBlock(), 
        use_json_field=True, 
        blank=True,
        verbose_name="主页内容区块"
    )

    # modify your content_panels:
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("header_background"),
                FieldPanel("image"),
                FieldPanel("hero_text"),
            ],
            heading="Hero section",
        ),
        FieldPanel('body'),
    ]