from django.contrib import admin

from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    list_display_links = ['pk', 'title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'views', 'display_image_in_admin', 'category', 'author']
    list_display_links = ['pk', 'title']
    list_filter = ['category', 'author', 'created_at']
    list_editable = ['category', 'author']
    readonly_fields = ['views']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment)
