# products/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)  # e.g., Mens, Womens, Children

    def __str__(self):
        return self.name

PRODUCT_TYPE_CHOICES = [
    ('TS', 'T-Shirt'),
    ('SW', 'Sweater'),
    ('TK', 'Tank Top'),
]

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=2, choices=PRODUCT_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True) # requires Pillow
    # = models.PositiveIntegerField(default=0)  # Inventory Tracking Field
    quantity = (models.IntegerField(default=0))

    def __str__(self):
        return self.name
