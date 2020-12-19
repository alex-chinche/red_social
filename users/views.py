from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            instance = User()
            instance.name = request.POST.get('name')
            instance.surnames = request.POST.get('surnames')
            instance.birthday = request.POST.get('birthday')
            instance.email = request.POST.get('email')
            instance.password = request.POST.get('password')
            instance.verified = False

            instance.save()
            return JsonResponse({'register': True})
        else:
            return JsonResponse({'register': False})

    else:
        form = UserForm()

    return render(request, 'login.html', {'form': form})


def main(request):
    return render(request, 'index.html')
