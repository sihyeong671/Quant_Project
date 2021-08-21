from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from users.models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"
    

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    ordering = ('-date_joined', 'username')
    list_display = (
        'get_profile_image', 'email', 'username', 'first_name',
        'last_name', 'is_staff', 'is_superuser'
    )
    list_display_links = (
        'get_profile_image', 'email', 'username', 'first_name',
        'last_name', 'is_staff', 'is_superuser'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    inlines = (ProfileInline, )
    
    def get_profile_image(self, obj):
        image = obj.profile.image
        
        if not image:
            return ''
        return mark_safe(f'<img src="{image.url}" style="width: 50px;">')
    
    get_profile_image.short_description = _('Profile Image')