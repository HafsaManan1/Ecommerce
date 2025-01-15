from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        super(ShippingForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({'placeholder': 'Full Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['address1'].widget.attrs.update({'placeholder': 'Address1'})
        self.fields['address2'].widget.attrs.update({'placeholder': 'Address2'})
        self.fields['city'].widget.attrs.update({'placeholder': 'City'})
        self.fields['state'].widget.attrs.update({'placeholder': 'State'})
        self.fields['zipcode'].widget.attrs.update({'placeholder': 'Zipcode'})