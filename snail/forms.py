from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES =(
    ("F", "Flutterwave"),
    ("P", "Paystack"),
)

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    shipping_address_1 = forms.CharField(required=False)
    nearest_bustop = forms.CharField(required=False)
    shipping_country = CountryField(blank_label="(Select country)").formfield(
        widget=CountrySelectWidget(attrs={
            'class': "form-control",
        }), required=False
    )
    shipping_state = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)
    set_default_shipping_address = forms.BooleanField(required=False)
    use_default_shipping_address = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class PaymentForm(forms.Form):
    phonenumber = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "type": "number"
    }))