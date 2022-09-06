from django.contrib import admin
from .models import *
from django.urls import reverse, path
from django.template.response import TemplateResponse


@admin.register(Article)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'author',
                    'created_at',
                    'get_category',
                    'tag_list',
                    'is_published',
                    )
    list_display_links = ('title', )
    list_editable = ('is_published', )
    list_filter = ('author', 'is_published', 'category')
    list_max_show_all = 20
    list_per_page = 20

    def get_category(self, obj):
        return obj.category

    # get_category.admin_order_field = 'category'
    get_category.short_description = 'category'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
