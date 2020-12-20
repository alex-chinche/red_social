from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserForm
from .models import User
from .constants import *
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from .coders.token import encode_token, decode_token
import hashlib


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            instance = User()
            instance.name = request.POST.get('name')
            instance.surnames = request.POST.get('surnames')
            instance.birthday = request.POST.get('birthday')
            instance.email = request.POST.get('email')
            instance.verified = False

            # Encrypt password
            password = request.POST.get('password')
            encoded_password = password.encode()
            hashed_password = hashlib.sha256(encoded_password).hexdigest()
            instance.password = hashed_password

            instance.save()

            token = encode_token(instance.email, password)

            # Send mail here
            context = {'name': instance.name,
                       'social_network': SOCIAL_NETWORK_NAME,
                       'url': request.get_host() + '/confirm_mail/' + token.decode('UTF-8')}
            template = get_template('emails/register_mail.html')
            content = template.render(context)
            email = EmailMultiAlternatives(
                SOCIAL_NETWORK_NAME + ' email confirmation',
                SOCIAL_NETWORK_NAME,
                settings.EMAIL_HOST_USER,
                [instance.email],
            )
            email.attach_alternative(content, 'text/html')
            email.send()
            # End mail

            return JsonResponse({'register': True, 'email': instance.email})
        else:
            return JsonResponse({'register': False})

    else:
        form = UserForm()

    return render(request, 'login.html', {'form': form})


def confirm_email(request, token):
    try:
        decoded_token = decode_token(token.encode('UTF-8'))
        print("DATOS: ", decoded_token['email'],
              " y ", decoded_token['password'])
        user_to_verify = User.objects.get(
            email=decoded_token['email'], password=decoded_token['password'])
        if user_to_verify.verified == False:
            user_to_verify.verified = True
            user_to_verify.save()
            return HttpResponse("Account created successfully! Return to the page and login.")
        elif user_to_verify.verified == True:
            return HttpResponse("Account already exists.")
    except:
        return HttpResponse("An error has ocurred.")


def main(request):
    return render(request, 'index.html')
