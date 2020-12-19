from django import forms
from .models import User
from django.core.exceptions import ValidationError


class UserForm(forms.Form):
    name = forms.CharField(max_length=20)
    surnames = forms.CharField(max_length=30)
    birthday = forms.DateField()
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    confirmPassword = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')

        if password != confirmPassword:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data