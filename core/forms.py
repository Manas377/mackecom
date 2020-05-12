from django import forms
from django.forms import ModelForm
from .models import Checkout, ShippingAddress, BillingAddress

STATE = [
    ("ND", "New Delhi"),
    ("UP", "Uttar Pradesh"),
    ("MP", "Madhya Pradesh"),
    ("MH", "Maharashtra"),
    ("GJ", "Gujrat"),
    ("AP", "Arunachal Pradesh"),
]

PAYMENT_MODE = [
    ("UPI","UPI"),
    ("NB", "Net Banking"),
    ("CDC", "Credit/Debit Card")
]


class CheckoutForm(forms.Form):
    apartment = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': "Apartment Number"
    }))
    address1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        "placeholder": "Address Line 1",
        "label": "Address 1"
    }))
    address2 = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Address Line 2, (optional)"
    }), max_length=200, required=False)
    state = forms.ChoiceField(widget=forms.Select, choices=STATE)
    zip = forms.IntegerField(max_value=999999)
    city = forms.CharField(max_length=20)
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_info = forms.ChoiceField(choices=PAYMENT_MODE)


class ShippingForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ("apartment", "address1", "address2", "state", "zip", "city")
        STATE = [
            ("ND", "New Delhi"),
            ("UP", "Uttar Pradesh"),
            ("MP", "Madhya Pradesh"),
            ("MH", "Maharashtra"),
            ("GJ", "Gujrat"),
            ("AP", "Arunachal Pradesh"),
        ]
        widgets = {
            'state': forms.Select(choices=STATE, attrs={'class': 'form-control'})
        }


class BillingForm(ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ["user"]


class CheckoutFormStructured(ModelForm):
    class Meta:
        model = Checkout
        fields = ("payment_info", "billing_same_as_shipping")
        PAYMENT_MODE = [
            ("UPI", "UPI"),
            ("NB", "Net Banking"),
            ("CDC", "Credit/Debit Card")
        ]
        widgets = {
            'payment_info': forms.Select(choices=PAYMENT_MODE, attrs={'class': 'form-control'})
        }
