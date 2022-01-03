from django.forms import forms

class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter you username'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter you email'}),required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter you password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Renter you password'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter you first name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter you last name'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')