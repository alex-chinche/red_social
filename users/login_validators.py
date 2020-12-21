import sys
from .coders.token import encode_token, decode_token, hash_password
import hashlib
from .models import User
from django.shortcuts import render, redirect


def auth_required(func):
    def internal_func(request, *args, **kwargs):
        readable_token = request.COOKIES.get('auth_token')
        encoded_token = decode_token(readable_token.encode('UTF-8'))
        email = encoded_token['email']
        password = encoded_token['password']
        myuser = User.objects.get(email=email, password=password)
        data = {'name': myuser.name}
        print("ESTAMODS EN LA FUNCION DECORADORA")
        print(data['name'])

        return func(request, data)
        
    return internal_func
