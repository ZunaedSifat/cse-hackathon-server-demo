from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=64)
    password = forms.CharField(max_length=64)
