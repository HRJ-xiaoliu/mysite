from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from home.models import GlobalSearchMixin

class Publication(Orderable):
    page = ParentalKey('ResearchPage', related_name='publications')
    title = models.CharField(max_length=255, verbose_name="成果标题")
    authors = models.CharField(max_length=500, verbose_name="作者列表")
    venue = models.CharField(max_length=255, verbose_name="发表平台/刊物")
    year = models.IntegerField(verbose_name="年份")
    pub_type = models.CharField(
        max_length=20, 
        choices=[('journal', '期刊论文'), ('conf', '会议文章'), ('patent', '授权专利')],
        default='journal'
    )
    doi = models.URLField(blank=True, default="", verbose_name="外部链接")
    
    bibtex_raw = models.TextField(blank=True, null=True, default="", verbose_name="BibTeX 原文 (用于批量导入解析参考)")
    
    abstract = RichTextField(blank=True, null=True, verbose_name="成果摘要")
    panels = [
        FieldPanel('title'),
        FieldPanel('authors'),
        FieldPanel('venue'),
        FieldPanel('year'),
        FieldPanel('pub_type'),
        FieldPanel('doi'),
        FieldPanel('abstract'),
    ]

class ResearchProject(Orderable):
    page = ParentalKey('ResearchPage', related_name='projects')
    title = models.CharField(max_length=255, verbose_name="项目名称")
    role = models.CharField(max_length=100, verbose_name="职责角色")
    status = models.CharField(max_length=100, verbose_name="项目编号/状态")
    description = RichTextField(blank=True, null=True, verbose_name="项目说明")
    panels = [
        FieldPanel('title'),
        FieldPanel('role'),
        FieldPanel('status'),
        FieldPanel('description'),
    ]

class ResearchPage( GlobalSearchMixin ):
    template = "research/research_index_page.html"
    intro = RichTextField(blank=True, null=True, verbose_name="研究方向综述")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('publications', label="学术论文与专利"),
        InlinePanel('projects', label="科研项目"),
    ]