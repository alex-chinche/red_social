from django import forms
from .models import User, Photo
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.Form):
    name = forms.CharField(max_length=20)
    surnames = forms.CharField(max_length=30)
    birthday = forms.DateField()
    email = forms.EmailField()
    password = forms.CharField(max_length=50)
    confirmPassword = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')

        if password != confirmPassword:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = self.cleaned_data

        return cleaned_data


class ProfilePicUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic']


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['picture']
