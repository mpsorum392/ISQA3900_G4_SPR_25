# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def products_by_category(request, category_name):
    # Assuming you have a Category model
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_list.html', {
        'category': category,
        'products': products
    })

