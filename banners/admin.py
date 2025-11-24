from django.contrib import admin

from .models import Banner, SubBanner


class BannerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_en',
        'title_ro',
        'sub_title_en',
        'sub_title_ro',
        'image',
        'text_color',
        'button_color',
        'button_text_color',
        'order'
    )
    list_editable = (
        'title_en',
        'title_ro',
        'sub_title_en',
        'sub_title_ro',
        'image',
        'text_color',
        'button_color',
        'button_text_color',
        'order'
    )

admin.site.register(Banner,BannerAdmin)



class SubBannerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_en',
        'title_ro',
        'sub_title_en',
        'sub_title_ro',
        'image',
        'text_color',
        'button_color',
        'button_text_color',
        'order'
    )
    list_editable = (
        'title_en',
        'title_ro',
        'sub_title_en',
        'sub_title_ro',
        'image',
        'text_color',
        'button_color',
        'button_text_color',
        'order'
    )

admin.site.register(SubBanner,SubBannerAdmin)
