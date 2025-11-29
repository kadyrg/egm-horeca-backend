from django.contrib import admin

from .models import Legal


class LegalAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'file')
    list_editable = ('type', 'file')

admin.site.register(Legal, LegalAdmin)
