from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def add_to_cart(request, product_id):
    """
    Adds a product to the session-based cart.
    Stores each product as a dict with 'quantity' and 'price'.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})

    product_key = str(product_id)
    if product_key in cart:
        # Increase the quantity if the product is already in the cart.
        cart[product_key]['quantity'] += 1
    else:
        # Otherwise, initialize it with quantity 1 and its price.
        cart[product_key] = {
            'quantity': 1,
            'price': str(product.price)  # Store as a string for session serialization.
        }

    # Save the cart back to the session.
    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    """
    Shows the cart items and calculates the total price.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    # Iterate over the cart dictionary.
    for product_id, item in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        quantity = item.get('quantity', 0)
        # Multiply product.price (a Decimal) with quantity (an integer)
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
