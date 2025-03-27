# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from products.models import Product


def add_to_cart(request, product_id):
    """
    Adds a product to the session-based cart.
    """
    product = get_object_or_404(Product, pk=product_id)

    # Retrieve the cart from the session or create an empty dict
    cart = request.session.get('cart', {})

    # Increase quantity if product already in cart, otherwise set to 1
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    # Save cart back to session
    request.session['cart'] = cart

    # Redirect to cart detail or wherever you'd like
    return redirect('cart_detail')


def cart_detail(request):
    """
    Shows the cart items and total price.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)
