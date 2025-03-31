from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from products.models import Product  # Import the updated Product model
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                # Create an OrderItem for each cart item.
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                # Update the product inventory using the "quantity" field.
                item['product'].quantity = item['product'].quantity - item['quantity']
                item['product'].save()
            # Clear the cart after processing the order.
            cart.clear()
            # Store the order id in the session.
            request.session['order_id'] = order.id

            return render(request, 'orders/create.html', {'order_id': order.id})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})
