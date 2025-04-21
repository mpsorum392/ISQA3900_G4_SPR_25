from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .models import Order, OrderItem
from .forms import OrderCreateForm, CreditCardForm
from cart.cart import Cart
from billing.models import Payment


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
            return redirect('orders:checkout', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {
        'cart': cart,
        'form': form,
    })


def checkout(request, order_id):
    """
    Step 2: Show shipping form + fake‑CC form on GET,
    process & immediately “confirm” payment on POST.
    """
    order = get_object_or_404(Order, id=order_id)

    # Shipping form pre‑populated (so user can review/edit)
    ship_form = OrderCreateForm(instance=order)

    if request.method == 'POST':
        cc_form = CreditCardForm(request.POST)
        if cc_form.is_valid():
            # 1) Create & confirm the dummy payment
            payment = Payment.objects.create(
                order=order,
                variant='default',
                description=f'Order #{order.id}',
                total=order.get_total(),
                tax=Decimal('0.00'),
                currency='USD',
            )
            payment.change_status('confirmed')

            # 2) Link & mark paid
            order.payment = payment
            order.paid    = True
            order.save()

            # 3) Redirect to receipt
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






