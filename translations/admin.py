from django.contrib import admin

from .models import Translation


class TranslationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value_en', 'value_ro')
    list_editable = ('value_en', 'value_ro')
    ordering = ('key',)

admin.site.register(Translation, TranslationAdmin)
