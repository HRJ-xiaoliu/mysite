from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from .blocks import HomeStreamBlock
from django.apps import apps
from wagtail.search import index
from django.utils.html import strip_tags
from wagtail.blocks import StreamValue
from django.db.models.manager import Manager

class GlobalSearchMixin(models.Model):
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

    search_fields = [
        index.SearchField('auto_search_text'),
    ]
    

class DynamicContentBlock(blocks.StructBlock):
    section_title = blocks.CharBlock(required=True, label="版块标题", help_text="例如：最新调研报告、现代诗歌精选")
    
    app_label_model = blocks.ChoiceBlock(
        choices=[
            ['research.ResearchPage', '学术研究与调研'], 
            ['blog.BlogPage', '新闻和文章'],
        ],
        label="数据来源",
        help_text="选择该版块要自动抓取并展示的内容类型"
    )
    
    item_count = blocks.IntegerBlock(default=4, min_value=1, max_value=12, label="展示数量")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        
        app_label, model_name = value.get('app_label_model').split('.')
        target_model = apps.get_model(app_label, model_name)
        
        context['latest_items'] = target_model.objects.live().order_by('-first_published_at')[:value.get('item_count')]
        return context

    class Meta:
        template = 'home/blocks/dynamic_content_block.html'
        icon = 'list-ul'
        label = '动态内容聚合版块'
    

class HomePage(Page, GlobalSearchMixin):
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
    
    body = StreamField(
        HomeStreamBlock(), 
        use_json_field=True, 
        blank=True,
        verbose_name="主页内容区块"
    )

    search_fields = Page.search_fields + GlobalSearchMixin.search_fields + [
        index.SearchField('hero_text'),
    ]

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