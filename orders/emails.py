from django.conf        import settings
from django.core.mail   import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils       import timezone

def send_order_confirmation(order):
    subject   = f'Your G4Threads Order #{order.id} Confirmation'
    from_email = settings.DEFAULT_FROM_EMAIL
    to         = [order.email]

    text_body = render_to_string('emails/order_confirmation.txt', {'order': order})
    html_body = render_to_string('emails/order_confirmation.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_body, from_email, to)
    msg.attach_alternative(html_body, "text/html")
    msg.send()

def send_account_update_notification(user):
    subject   = 'Your G4Threads Account Settings Have Changed'
    from_email = settings.DEFAULT_FROM_EMAIL
    to         = [user.email]
    context    = {
        'user':      user,
        'timestamp': timezone.now(),
    }

    text_body = render_to_string('emails/account_update.txt', context)
    html_body = render_to_string('emails/account_update.html', context)

    msg = EmailMultiAlternatives(subject, text_body, from_email, to)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
