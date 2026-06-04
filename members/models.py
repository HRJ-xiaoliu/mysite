from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from home.models import GlobalSearchMixin

class MemberSdPage(Page, GlobalSearchMixin):
    template = "members/member_sd.html"

    STATUS_CHOICES = [
        ('enrolled', '在读'),
        ('graduated', '已毕业'),
    ]

    DEGREE_CHOICES = [
        ('master', '硕士'),
        ('phd', '博士'),
        ('postdoc', '博士后'),
    ]

    avatar = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+', verbose_name="成员头像"
    )
    
    academic_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='enrolled', verbose_name="学业状态"
    )
    
    degree_type = models.CharField(
        max_length=20, choices=DEGREE_CHOICES, default='master', verbose_name="攻读/获得学位"
    )
    
    birth_date = models.DateField("出生年月", null=True, blank=True)
    
    enrollment_year = models.IntegerField("入学年份", null=True, blank=True, help_text="例如：2023")

    dynamic_content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", label="章节标题")),
        ('paragraph', blocks.RichTextBlock(label="富文本内容")),
        ('image', ImageChooserBlock(label="插图")),
    ], use_json_field=True, blank=True, verbose_name="详细信息拓展区")

    search_fields = Page.search_fields + [
        index.SearchField('academic_status'),
        index.SearchField('degree_type'),
        index.SearchField('dynamic_content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('avatar'),
        FieldPanel('academic_status'),
        FieldPanel('degree_type'),
        FieldPanel('birth_date'),
        FieldPanel('enrollment_year'),
        FieldPanel('dynamic_content'),
    ]


class MemberTcPage(Page, GlobalSearchMixin):
    template = "members/member_tc.html"

    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    avatar = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+', verbose_name="教师头像"
    )
    
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='male', verbose_name="性别"
    )
    
    professional_title = models.CharField(
        max_length=100, verbose_name="职称", help_text="例如：教授、副教授、特聘研究员等"
    )
    
    research_direction = models.CharField(
        max_length=255, verbose_name="主要研究方向", help_text="请简要描述您的学术研究领域"
    )

    dynamic_content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", label="章节标题")),
        ('paragraph', blocks.RichTextBlock(label="详细介绍内容")),
        ('image', ImageChooserBlock(label="相关插图")),
    ], use_json_field=True, blank=True, verbose_name="其他信息展示区")

    search_fields = Page.search_fields + [
        index.SearchField('professional_title'),
        index.SearchField('research_direction'),
        index.SearchField('dynamic_content'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('avatar'),
        FieldPanel('gender'),
        FieldPanel('professional_title'),
        FieldPanel('research_direction'),
        FieldPanel('dynamic_content'),
    ]


class MemberIndexPage(Page, GlobalSearchMixin):
    template = "members/member_index_page.html"
    
    intro = RichTextField(blank=True, verbose_name="页面简介")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        teachers = MemberTcPage.objects.live().descendant_of(self).order_by('title')
        students = MemberSdPage.objects.live().descendant_of(self).order_by('title')
        
        context['teachers'] = teachers
        context['students'] = students
        
        return context