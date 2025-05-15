from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def cart_add(request, product_id):
    """
    Adds one unit of the given product to the session-based cart.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})

    key = str(product_id)
    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'quantity': 1,
            'price': str(product.price),
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart:cart_detail')


def cart_update(request, product_id):
    """
    Updates the quantity of a product in the cart.
    If quantity <= 0, removes the item.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    key = str(product_id)

    try:
        qty = int(request.POST.get('quantity', 0))
    except (ValueError, TypeError):
        qty = 0

    if qty > 0:
        cart[key] = {
            'quantity': qty,
            'price': str(product.price),
        }
    else:
        cart.pop(key, None)

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """
    Removes the given product entirely from the session-based cart.
    """
    cart = request.session.get('cart', {})
    key = str(product_id)

    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Renders the cart: a list of items plus the total price.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pid_str, item in cart.items():
        pid = int(pid_str)
        product = get_object_or_404(Product, pk=pid)
        quantity = item.get('quantity', 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product':  product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total':      total,
    })



