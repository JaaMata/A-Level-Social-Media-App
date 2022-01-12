from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter you username'}),
                               required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter you email'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter you password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Renter you password'}), required=True)
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter you first name'}),
                                 required=True)
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter you last name'}),
                                required=True)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.get(username=username) is not None:
            raise forms.ValidationError('The username enterd is already entered')

        if not len(password1) >= 8:
            raise forms.ValidationError('The password entred is less then 8 characters.')

        if not password1 == password2:
            raise forms.ValidationError("The passwords entered don't match.")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter you username'}),
                               required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Enter you password'}), required=True)

    def clean(self):

        return True
    # todo: Input sanitisation
