from django.contrib import admin

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from boards.models import Board, Category, Comment, Reply


class CategoryInline(admin.StackedInline):
    model = Category
    can_delete = False
    verbose_name_plural = "categories"
    
class BoardInline(admin.StackedInline):
    model = Board
    can_delete = False
    verbose_name_plural = "boards"

class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = False
    verbose_name_plural = "comments"


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
    inlines = (BoardInline, )
    
    def get_creator(self, obj):
        creator = obj.creator.profile.nickname
        return creator
    get_creator.short_description = _("creator")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    ordering = ('-created_date', 'creator__profile__nickname')
    list_display = (
        'get_thumbnail_image', 'category', 'title', 'content', 'get_creator', 'hits',
        'top_fixed', 'get_creator', 'get_favorit_count'
    )
    list_display_links = (
        'get_thumbnail_image', 'category', 'title', 'content', 'get_creator', 'hits',
        'top_fixed', 'get_creator', 'get_favorit_count'
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
    
    
    def get_favorit_count(self, obj):
        cnt = obj.favorite.count()
        return cnt
    get_favorit_count.short_description = _("favorite_count")
    
    