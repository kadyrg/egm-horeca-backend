from django.contrib import admin

from products.models import Product
from .models import Category, SubCategory


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = (SubCategoryInline, )
    list_display = (
        'id',
        'order',
        'title_en',
        'title_ro',
        'meta_title_en',
        'meta_title_ro',
        'meta_description_en',
        'meta_description_ro',
    )
    list_editable = (
        'order',
        'title_en',
        'title_ro',
        'meta_title_en',
        'meta_title_ro',
        'meta_description_en',
        'meta_description_ro',
    )
    search_fields = (
        'title_en',
        'title_ro',
        'meta_title_en',
        'meta_title_ro',
        'meta_description_en',
        'meta_description_ro',
    )
    ordering = ('order',)
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title_en',
                'title_ro',
                'meta_title_en',
                'meta_title_ro',
                'meta_description_en',
                'meta_description_ro'
            ),
        }),
        ('Ordering', {
            'fields': ('order',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('slug', 'created_at', 'updated_at')

admin.site.register(Category, CategoryAdmin)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class SubCategoryAdmin(admin.ModelAdmin):
    inlines = (ProductInline, )
    list_display = (
        'id',
        'order',
        'title_en',
        'title_ro',
        'category',
    )
    list_editable = (
        'order',
        'title_en',
        'title_ro',
        'category',
    )
    search_fields = (
        'title_en',
        'title_ro',
    )
    list_filter = (
        'category',
    )
    ordering = ('order',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('title_en', 'title_ro', 'category')
        }),
        ('Ordering', {
            'fields': ('order',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(SubCategory, SubCategoryAdmin)
