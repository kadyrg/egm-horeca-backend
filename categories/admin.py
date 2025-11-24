from django.contrib import admin

from .models import Category, SubCategory


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = (SubCategoryInline, )
    list_display = (
        'id',
        'title_en',
        'title_ro',
        'meta_title_en',
        'meta_title_ro',
        'meta_description_en',
        'meta_description_ro',
        'order',
    )
    list_editable = (
        'title_en',
        'title_ro',
        'meta_title_en',
        'meta_title_ro',
        'meta_description_en',
        'meta_description_ro',
        'order',
    )

admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'title_en',
        'title_ro',
        'order'
    )
    list_editable = (
        'category',
        'title_en',
        'title_ro',
        'order'
    )

admin.site.register(SubCategory, SubCategoryAdmin)
