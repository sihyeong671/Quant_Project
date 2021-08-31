from django.contrib import admin

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from boards.models import Post, Category, Comment, Reply


class CategoryInline(admin.StackedInline):
    model = Category
    can_delete = False
    verbose_name_plural = "categories"
    
class PostInline(admin.StackedInline):
    model = Post
    can_delete = False
    verbose_name_plural = "posts"

class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = False
    verbose_name_plural = "comments"

class ReplyInline(admin.StackedInline):
    model = Reply
    can_delete = False
    verbose_name_plural = 'replies'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('-created_date', 'creator__profile__nickname')
    list_display = (
        'title', 'is_anonymous', 'created_date', 'top_fixed',
        'get_creator',
    )
    list_display_links = (
        'title', 'is_anonymous', 'created_date', 'top_fixed',
        'get_creator',
    )
    search_fields = ('created_date', 'creator__profile__nickname', 'title', )
    inlines = (PostInline, )
    
    def get_creator(self, obj):
        creator = obj.creator.profile.nickname
        return creator
    get_creator.short_description = _("creator")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ('-created_date', 'creator__profile__nickname')
    list_display = (
        'get_thumbnail_image', 'category', 'title', 'content', 'get_creator', 'hits',
        'top_fixed', 'get_creator',
    )
    list_display_links = (
        'get_thumbnail_image', 'category', 'title', 'content', 'get_creator', 'hits',
        'top_fixed', 'get_creator',
    )
    search_fields = ('created_date', 'creator__profile__nickname', 'title', 'category__title')
    list_filter = ('category__title', )
    
    inlines = (CommentInline, )
    
    def get_thumbnail_image(self, obj):
        image = obj.thumbnail
        
        if not image:
            return ''
        return mark_safe(f'<img src="{image.url}" style="width: 50px;">')
    get_thumbnail_image.short_description = _('Thumbnail Image')
    
    
    def get_creator(self, obj):
        creator = obj.creator.profile.nickname
        return creator
    get_creator.short_description = _("creator")
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_post', 'content', 'get_creator',
    )
    list_display_links = (
        'id', 'get_post', 'content', 'get_creator',
    )
    search_fields = ('created_date', 'creator__profile__nickname', 'post__title')
    list_filter = ('post__title', )
    
    inlines = (ReplyInline, )
    
    def get_creator(self, obj):
        creator = obj.creator.profile.nickname
        return creator
    get_creator.short_description = _("creator")
    
    def get_post(self, obj):
        post = obj.post.title
        return post
    get_post.short_description = _("post")
    