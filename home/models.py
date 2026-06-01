from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
# import MultiFieldPanel:
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from .blocks import HomeStreamBlock
from django.apps import apps
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
    
class DynamicContentBlock(blocks.StructBlock):
    """[核心逻辑] 这是一个结构化区块，允许你在主页自由添加多个这样的版块，你可以随意上下拖拽改变它们的排列顺序。"""
    section_title = blocks.CharBlock(required=True, label="版块标题", help_text="例如：最新调研报告、现代诗歌精选")
    
    # [需修改] 这里是数据流向的“开关”。
    # 列表的左侧是 '应用名.模型名'，右侧是后台显示的中文标签。
    # 你需要根据你实际创建的应用（app）名称和模型（Model）名称进行替换。
    app_label_model = blocks.ChoiceBlock(
        choices=[
            # 假设你有一个名为 research 的 app，里面有一个 ResearchPage 模型
            ['research.ResearchPage', '学术研究与调研'], 
            
            # 假设你有一个名为 poetry 的 app，专门存放你的现代诗作品
            ['blog.BlogPage', '新闻和文章'],
        ],
        label="数据来源",
        help_text="选择该版块要自动抓取并展示的内容类型"
    )
    
    item_count = blocks.IntegerBlock(default=4, min_value=1, max_value=12, label="展示数量")

    def get_context(self, value, parent_context=None):
        """
        [核心逻辑] 这个方法是跨应用抓取数据的引擎。
        它会根据你在后台选择的 'app_label_model'，动态去数据库里拉取对应的数据。
        """
        context = super().get_context(value, parent_context=parent_context)
        
        # 将 'research.ResearchPage' 拆分成 'research' 和 'ResearchPage'
        app_label, model_name = value.get('app_label_model').split('.')
        
        # 动态获取对应的模型类
        target_model = apps.get_model(app_label, model_name)
        
        # [核心逻辑] 过滤出已发布 (live) 的页面，并按照首次发布时间倒序排列 (-first_published_at)
        # 如果你想改为按后台手动排序，可以将 '-first_published_at' 改为其他的排序字段
        context['latest_items'] = target_model.objects.live().order_by('-first_published_at')[:value.get('item_count')]
        return context
    class Meta:
        # [需修改] 确保你的项目中存在这个 HTML 模板文件。
        # 路径通常是你的 home 应用下的 templates/blocks/dynamic_content_block.html
        template = 'home/blocks/dynamic_content_block.html'
        icon = 'list-ul'
        label = '动态内容聚合版块'
    

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