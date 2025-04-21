# billing/admin.py

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ('id', 'order', 'status', 'total', 'transaction_id', 'created')
    list_filter   = ('status', 'created')
    search_fields = ('order__id', 'transaction_id')
