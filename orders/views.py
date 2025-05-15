from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from .models import Order, OrderItem
from .forms import OrderCreateForm, CreditCardForm
from cart.cart import Cart
from billing.models import Payment
from .emails import send_order_confirmation  # ← import the helper

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
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                item['product'].quantity -= item['quantity']
                item['product'].save()
            cart.clear()

            # ─── send the confirmation email ────────────────────────
            send_order_confirmation(order)
            # ─────────────────────────────────────────────────────────

            return redirect('orders:checkout', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {
        'cart': cart,
        'form': form,
    })

def checkout(request, order_id):
    """
    Step 2: Show shipping form + fake-CC form on GET,
    process & immediately “confirm” payment on POST.
    """
    order = get_object_or_404(Order, id=order_id)
    ship_form = OrderCreateForm(instance=order)

    if request.method == 'POST':
        cc_form = CreditCardForm(request.POST)
        if cc_form.is_valid():
            payment = Payment.objects.create(
                order=order,
                variant='default',
                description=f'Order #{order.id}',
                total=order.get_total(),
                tax=Decimal('0.00'),
                currency='USD',
            )
            payment.change_status('confirmed')

            order.payment = payment
            order.paid    = True
            order.save()

            return redirect('orders:receipt', order_id=order.id)
    else:
        cc_form = CreditCardForm()

    return render(request, 'orders/checkout.html', {
        'order':   order,
        'form':    ship_form,
        'cc_form': cc_form,
    })

def receipt(request, order_id):
    """
    Step 3: Display the outcome.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/receipt.html', {
        'order': order,
    })






