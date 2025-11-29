from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'label_en', 'label_ro', 'link')
    list_editable = ('label_en', 'label_ro', 'link')

admin.site.register(Contact, ContactAdmin)
