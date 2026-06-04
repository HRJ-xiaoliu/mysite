from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from home.models import GlobalSearchMixin

class BlogIndexPage(Page, GlobalSearchMixin):
    intro = RichTextField(blank=True, verbose_name="页面简介")

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    def get_context(self, request):
        context = super().get_context(request)
       
        all_posts = self.get_children().live().order_by('-first_published_at')
        
        paginator = Paginator(all_posts, 6) 
        page = request.GET.get('page')
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            
        context['page_obj'] = posts
        context['paginator'] = paginator
        context['tag_index_page'] = BlogTagIndexPage.objects.first()
        return context
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

@register_snippet
class Author(models.Model, index.Indexed):
    name = models.CharField(max_length=255, verbose_name="姓名")
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+', verbose_name="头像"
    )
    
    search_fields = [
        index.SearchField('name', partial_match=True),
    ]
    
    panels = [
        FieldPanel("name"),
        FieldPanel("author_image"),
    ]
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'Authors'

class BlogPage(Page, GlobalSearchMixin):
    subtitle = models.CharField(max_length=255, blank=True, null=True, default="这是一个副标题", verbose_name="副标题")
    article_source = models.CharField(max_length=100, blank=True, null=True, default="新闻网", verbose_name="来源")
    intro = models.TextField(blank=True, verbose_name="文章导语")
    body = RichTextField(verbose_name="正文")
    editor = models.CharField(max_length=50, blank=True, null=True, verbose_name="编辑")
    reviewer = models.CharField(max_length=50, blank=True, null=True, verbose_name="审核")
    reading_time = models.IntegerField(blank=True, null=True, verbose_name="预计阅读时间")
    
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True, verbose_name="分类标签")
    authors = ParentalManyToManyField('blog.Author', blank=True, verbose_name="文章作者")

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        return None

    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('article_source'),
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('editor'),
        index.SearchField('reviewer'),
        index.RelatedFields('authors', [
            index.SearchField('name', partial_match=True),
        ]),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('authors'),
            FieldPanel('reading_time'),
            FieldPanel('tags'),
        ], heading="文章元数据"),
        MultiFieldPanel([
            FieldPanel('subtitle'),
            FieldPanel('article_source'),
            FieldPanel('intro'),
            FieldPanel('body'),
        ], heading="主体内容"),
        MultiFieldPanel([
            FieldPanel('editor'),
            FieldPanel('reviewer'),
        ], heading="内部控制信息"),
        InlinePanel("gallery_images", label="图像资料库"),
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250, verbose_name="图片脚注")
    
    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

class BlogTagIndexPage(Page, GlobalSearchMixin):
    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context