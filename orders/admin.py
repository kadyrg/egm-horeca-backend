from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'phone_number',
        'entity_type',
        'first_name',
        'last_name',
        'status',
        'country',
        'city',
        'postal_code',
        'street',
        'house_number',
        'created_at'
    )
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)
