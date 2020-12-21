import sys
from .coders.token import encode_token, decode_token, hash_password
import hashlib
from .models import User
from django.shortcuts import render, redirect


def auth_required(func):
    def internal_func(request, *args, **kwargs):
        try:
            readable_token = request.COOKIES.get('auth_token')
            encoded_token = decode_token(readable_token.encode('UTF-8'))
            email = encoded_token['email']
            password = encoded_token['password']
            User.objects.get(email=email, password=password)
            return func(request, *args, **kwargs)
        except:
            return redirect('/')
    return internal_func
