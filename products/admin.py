from django.contrib import admin

from .models import Product, ProductImage, ProductAttribute, ProductAttributeItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline, ProductAttributeInline)
    list_display = (
        'id',
        'order',
        'title_en',
        'title_ro',
        'description_en',
        'description_ro',
        'old_price',
        'brand_title',
        'price',
        'stock',
        'main_image',
        'is_active',
        'category',
        'slug'
    )
    readonly_fields = ('slug', 'created_at', 'updated_at')
    list_editable = (
        'order',
        'title_en',
        'title_ro',
        'description_en',
        'description_ro',
        'old_price',
        'brand_title',
        'price',
        'stock',
        'main_image',
        'is_active',
        'category',
    )
    ordering = ('order',)
    search_fields = ('title_en', 'title_ro', 'description_en', 'description_ro')
    list_filter = ('is_active', 'category')
    fieldsets = (
        ('Basic Info', {
            'fields': (
                'title_en',
                'title_ro',
                'description_en',
                'description_ro',
                'old_price',
                'price',
                'stock',
                'main_image',
                'is_active',
                'category'
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

admin.site.register(Product, ProductAdmin)



class ProductAttributeItemInline(admin.TabularInline):
    model = ProductAttributeItem
    extra = 1

class ProductAttributeAdmin(admin.ModelAdmin):
    inlines = (ProductAttributeItemInline,)
    list_display = (
        'id',
        'product',
        'title_en',
        'title_ro',
    )
    list_editable = (
        'product',
        'title_en',
        'title_ro',
    )
    search_fields = ('title_en', 'title_ro')
    list_filter = ('product', )
    fieldsets = (
        ('Basic Info', {
            'fields': ('title_en', 'title_ro', 'product'),
        }),
    )

admin.site.register(ProductAttribute, ProductAttributeAdmin)


class ProductAttributeItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_en',
        'title_ro',
        'attribute',
        'old_price',
        'price',
        'stock',
    )
    list_editable = (
        'title_en',
        'title_ro',
        'attribute',
        'old_price',
        'price',
        'stock',
    )
    search_fields = ('title_en', 'title_ro')
    list_filter = ('attribute', )
    fieldsets = (
        ('Basic Info', {
            'fields': ('title_en', 'title_ro', 'attribute', 'old_price', 'price', 'stock'),
        }),
    )

admin.site.register(ProductAttributeItem, ProductAttributeItemAdmin)
