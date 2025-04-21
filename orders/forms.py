# orders/forms.py

from django import forms
from .models import Order
from datetime import datetime

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

class CreditCardForm(forms.Form):
    card_number = forms.CharField(
        label="Card Number", max_length=19,
        widget=forms.TextInput(attrs={"placeholder": "1234 5678 9012 3456"})
    )
    exp_month = forms.ChoiceField(
        label="Expiry Month",
        choices=[(f"{m:02}", f"{m:02}") for m in range(1,13)]
    )
    exp_year = forms.ChoiceField(
        label="Expiry Year",
        choices=[(str(y), str(y)) for y in range(datetime.now().year, datetime.now().year+11)]
    )
    cvv = forms.CharField(
        label="CVV", max_length=4,
        widget=forms.PasswordInput(attrs={"placeholder": "123"})
    )