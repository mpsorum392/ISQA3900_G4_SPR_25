from django.db import models
from payments.models import BasePayment

class Payment(BasePayment):
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payments'
    )
