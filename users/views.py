from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm
from .models import User
from .constants import *
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from .coders.token import encode_token, decode_token, hash_password
import hashlib
from .login_validators import auth_required


def main(request):
    token = request.COOKIES.get('auth_token')
    print(token)
    return render(request, 'main.html')


@auth_required
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.is_ajax():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                name = request.POST.get('name')
                surnames = request.POST.get('surnames')
                birthday = request.POST.get('birthday')
                email = request.POST.get('email')
                password = request.POST.get('password')
                # Encrypt password
                hashed_password = hash_password(password)

                User(name=name, surnames=surnames,
                     birthday=birthday, email=email, password=hashed_password, verified=False).save()

                encoded_token = encode_token(email, hashed_password)
                readable_token = encoded_token.decode('UTF-8')

                # Send mail here
                context = {'name': name,
                           'social_network': SOCIAL_NETWORK_NAME,
                           'url': request.get_host() + '/confirm/' + readable_token}
                template = get_template('emails/register_mail.html')
                content = template.render(context)
                mail = EmailMultiAlternatives(
                    SOCIAL_NETWORK_NAME + ' email confirmation',
                    SOCIAL_NETWORK_NAME,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                mail.attach_alternative(content, 'text/html')
                mail.send()
                # End mail

                return JsonResponse({'register': True, 'email': email})
            else:
                return JsonResponse({'register': False})
        else:
            return JsonResponse({'register': False})
    else:
        return redirect('/')


def confirm_email(request, token):
    try:
        encoded_token = decode_token(token.encode('UTF-8'))
        user_to_verify = User.objects.get(
            email=encoded_token['email'], password=encoded_token['password'])
        if user_to_verify.verified == False:
            user_to_verify.verified = True
            user_to_verify.save()
            return HttpResponse("Account created successfully! Return to the page and login.")
        elif user_to_verify.verified == True:
            return HttpResponse("Account already exists.")
    except:
        return HttpResponse("An error has ocurred.")


def login(request):
    if request.is_ajax():
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                password = request.POST.get('password')
                hashed_password = hash_password(password)
                try:
                    User.objects.get(email=email, password=hashed_password)
                    # Save token in cookies
                    encoded_token = encode_token(email, hashed_password)
                    readable_token = encoded_token.decode('UTF-8')

                    return JsonResponse({'login': True, 'token': readable_token})
                except:
                    return JsonResponse({'login': False})
            else:
                return JsonResponse({'login': False})
        else:
            return JsonResponse({'login': False})
    else:
        return redirect('/')
