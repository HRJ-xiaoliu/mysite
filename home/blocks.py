from wagtail.blocks import (
    CharBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    ListBlock,
    DateBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageBlock, ImageChooserBlock

class HeroSlideBlock(StructBlock):
    image = ImageChooserBlock(label="轮播图片", required=True)
    link_page = PageChooserBlock(
        label="内部跳转页面", 
        required=False, 
        help_text="优先项：点击选择本站内部的具体页面，自动生成防丢链接"
    )
    link_external = URLBlock(
        label="外部跳转链接", 
        required=False, 
        help_text="备选项：如果需要跳转到外网（如百度、GitHub），请在此处填写完整 URL"
    )

    class Meta:
        icon = 'image'
        label = '单张幻灯片'
        
class HeroCarouselBlock(StructBlock):
    slides = ListBlock(HeroSlideBlock(), label="幻灯片集合")
    
    # 以后如果想加 "播放速度"、"轮播大标题" 等字段，直接写在这里即可！

    class Meta:
        template = "home/blocks/hero_block.html"
        icon = "images"
        label = "全屏轮播图区块"
        
class NewsItemBlock(StructBlock):
    title = CharBlock()
    summary = RichTextBlock()
    date = DateBlock()
    link = URLBlock(required=False)

class NewsBlock(StructBlock):
    title = CharBlock(default="新闻动态")
    subtitle = CharBlock(default="NEWS", required=False)
    news_items = ListBlock(NewsItemBlock())
    view_more_link = URLBlock(required=False)

    class Meta:
        template = "home/blocks/news_block.html"

class MediaItemBlock(StructBlock):
    source = CharBlock()
    title = CharBlock()
    link = URLBlock(required=False)
    date = CharBlock()

class MediaBlock(StructBlock):
    title = CharBlock(default="媒体报道")
    subtitle = CharBlock(default="MEDIA", required=False)
    media_items = ListBlock(MediaItemBlock())

    class Meta:
        template = "home/blocks/media_block.html"

class EventBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock()
    time = CharBlock()
    location = CharBlock()

class EventsBlock(StructBlock):
    title = CharBlock(default="活动预告")
    subtitle = CharBlock(default="EVENTS", required=False)
    events = ListBlock(EventBlock())
    view_more_link = URLBlock(required=False)

    class Meta:
        template = "home/blocks/events_block.html"


class EducationItemBlock(StructBlock):
    image = ImageChooserBlock(required=False, label="相关图片")
    title = CharBlock(required=True, label="经历标题")
    time = CharBlock(required=False, label="时间范围")
    location = CharBlock(required=False, label="地点")
    description = RichTextBlock(required=False, label="详细描述")

    class Meta:
        icon = "doc-full"
        label = "单项教育经历"

class EducationBlock(StructBlock):
    title = CharBlock(default="教育教学", required=True)
    subtitle = CharBlock(default="EDUCATION", required=False)
    education = ListBlock(EducationItemBlock(), label="教育经历列表")
    view_more_link = URLBlock(required=False, label="查看更多链接")

    class Meta:
        template = "home/blocks/education_block.html"
        icon = "list-ul"

class ResearchItemBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock()

class ResearchBlock(StructBlock):
    title = CharBlock(default="科学研究")
    subtitle = CharBlock(default="RESEARCH", required=False)
    research_items = ListBlock(ResearchItemBlock())
    view_more_link = URLBlock(required=False)

    class Meta:
        template = "home/blocks/research_block.html"

class HomeStreamBlock(StreamBlock):
    hero = HeroCarouselBlock()
    news = NewsBlock()
    media = MediaBlock()
    events = EventsBlock()
    education = EducationBlock()
    research = ResearchBlock()