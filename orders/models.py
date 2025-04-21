# orders/models.py

from django.db import models
from products.models import Product
from decimal import Decimal

class Order(models.Model):
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    email        = models.EmailField()
    address      = models.CharField(max_length=250)
    postal_code  = models.CharField(max_length=20)
    city         = models.CharField(max_length=100)
    created      = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)
    paid         = models.BooleanField(default=False)

    # ── NEW ── link to the dummy‑gateway payment record
    payment = models.ForeignKey(
        'billing.Payment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self) -> Decimal:
        """Sum of all line‑item costs."""
        return sum(item.get_cost() for item in self.items.all())

    # ── NEW ── alias for use by django‑payments in checkout view
    def get_total(self) -> Decimal:
        return self.get_total_cost()


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price    = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderItem {self.id}'

    def get_cost(self) -> Decimal:
        return self.price * self.quantity

