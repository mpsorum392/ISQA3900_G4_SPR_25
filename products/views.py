# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def products_by_category(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_list.html', {
        'category': category,
        'products': products,
    })

def search(request):
    q = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=q) if q else []
    return render(request, 'products/search_results.html', {
        'query': q,
        'results': results,
    })



