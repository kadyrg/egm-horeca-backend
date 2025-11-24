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
    list_editable = (
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
    readonly_fields = ('slug', )

admin.site.register(Product, ProductAdmin)



class ProductAttributeItemInline(admin.TabularInline):
    model = ProductAttributeItem
    extra = 1

class ProductAttributeAdmin(admin.ModelAdmin):
    inlines = (ProductAttributeItemInline,)
    list_display = (
        'id',
        'title_en',
        'title_ro',
        'product',
    )
    list_editable = (
        'title_en',
        'title_ro',
        'product',
    )

admin.site.register(ProductAttribute, ProductAttributeAdmin)
