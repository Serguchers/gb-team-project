from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import BaseUser, UserProfile


@admin.register(BaseUser)
class UserAdmin(admin.ModelAdmin):

    list_editable = ('is_active',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    def get_profile(self, obj):
        url = reverse('admin:userapp_userprofile_change', args=(obj.userprofile.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.userprofile.user)

    get_profile.admin_order_field = 'username'
    get_profile.short_description = 'profile'

    list_display = ('username',
                    'email',
                    'last_login',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                    'get_profile',
                    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'birth_date', 'user_id')
