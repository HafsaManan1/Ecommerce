from django import forms
from .models import ShippingAddress
from django.core.exceptions import ValidationError
import re

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

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[A-Za-z\s]+$', full_name):
            raise ValidationError('Full Name should only contain alphabets and spaces.')
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValidationError('Enter a valid email address.')
        return email

    def clean_address1(self):
        address1 = self.cleaned_data.get('address1')
        if not address1:
            raise ValidationError('Address1 is required.')
        return address1

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not re.match(r'^[A-Za-z\s]+$', city):
            raise ValidationError('City should only contain alphabets and spaces.')
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if not re.match(r'^[A-Za-z\s]+$', state):
            raise ValidationError('State should only contain alphabets and spaces.')
        return state

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')
        if not re.match(r'^\d{5}(-\d{4})?$', zipcode):
            raise ValidationError('Enter a valid zipcode (e.g., 12345 or 12345-6789).')
        return zipcode