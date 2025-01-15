from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

import re

# Registration Form

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['email'].required = True

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError("This email is invalid")
        
        if len(email) >= 50:
            raise forms.ValidationError("Your email is too long")
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Regular expression to enforce the rule
        # Starts with alphabet, followed by optional alphanumeric/special characters
        pattern = r'^[a-zA-Z]+[\w@#$%^&+=]*$'

        if not re.match(pattern, username):
            raise forms.ValidationError(
                "Username must start with letters and can contain numbers or special characters."
            )
        return username
    
# Login Form

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))

# Update Form

class UpdateUserForm(forms.ModelForm):

    password = None

    class Meta:

        model = User

        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        
        self.fields['email'].required = True


    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():

            raise forms.ValidationError("This email is invalid")
        
        if len(email) >= 350:
            raise forms.ValidationError("Your email is too long")
        
        return email

from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
            # 'class': 'form-control',  # Optional: Add custom CSS classes
        })

from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize password1 field
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter new password',
        })
        # Customize password2 field
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password',
        })