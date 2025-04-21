import csv
import datetime
from decimal import Decimal
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem
from billing.models import Payment


def order_detail(obj):
    # now points at the namespaced admin_order_detail view
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')
order_detail.short_description = "Details"


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
    writer = csv.writer(response)
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # header row
    writer.writerow([field.verbose_name for field in fields])
    # data rows
    for obj in queryset:
        row = []
        for field in fields:
            val = getattr(obj, field.name)
            if isinstance(val, datetime.datetime):
                val = val.strftime('%Y-%m-%d %H:%M')
            row.append(val)
        writer.writerow(row)
    return response
export_to_csv.short_description = "Export to CSV"


def refund_orders(modeladmin, request, queryset):
    for order in queryset:
        if order.payment:
            order.payment.change_status('refunded')
            order.paid = False
            order.save()
    modeladmin.message_user(request, "Selected orders have been refunded.")
refund_orders.short_description = "Refund selected orders"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'price', 'quantity')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = (
        'id', 'first_name', 'last_name', 'email',
        'paid', 'created', 'updated', order_detail
    )
    list_filter     = ('paid', 'created', 'updated')
    readonly_fields = ('payment',)
    inlines         = [OrderItemInline]
    actions         = [export_to_csv, refund_orders]

