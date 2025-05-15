# products/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product

def products_by_category(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_list.html', {
        'category': category,
        'products': products,
    })

def search(request):
    raw_q = request.GET.get('q', '')
    q     = raw_q.strip()

    if q:
        # search name OR description
        results = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
        # <-- DEBUG OUTPUT (should appear in your runserver console) -->
        print("🔍 SQL:", results.query)
        print("📝 Count:", results.count())
    else:
        results = Product.objects.none()

    return render(request, 'products/search_results.html', {
        'query': raw_q,
        'results': results,
    })


