from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm, ProfilePicUploadForm, PhotoUploadForm
from .models import User, Friend_Request, Photo
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
from django.templatetags.static import static
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone


def main(request):
    token = request.COOKIES.get('auth_token')
    if token:
        return redirect('/home')
    else:
        return render(request, 'main.html')


@auth_required
def home(request, mydata):
    return render(request, 'home.html', {'mydata': mydata})


@auth_required
def send_pulse(request, mydata):
    if request.is_ajax():
        try:
            mydata.last_connection = timezone.now()
            mydata.save()
            return JsonResponse({'connected': True})
        except:
            return JsonResponse({'connected': False})
    else:
        return redirect('/')


@auth_required
def get_friend_list(request, mydata):
    friends_list = User.objects.filter(id__in=mydata.friends.through.objects.filter(
        from_user_id=mydata.id).values('to_user_id')).order_by('name')
    number_of_connected_friends = 0
    number_of_friends = 0
    friends_html = ''
    for friend in friends_list:
        number_of_friends = number_of_friends + 1
        friends_html += '<div style="display:inline">' + '<p class="status '
        if friend.last_connection > timezone.now() - timedelta(seconds=30):
            friends_html += 'available'
            number_of_connected_friends = number_of_connected_friends + 1
        else:
            friends_html += 'disconnected'
        friends_html += '">•</p> ' + \
            friend.name + ' ' + friend.surnames + '</div>'
        friends_html += '<hr class="clear hr-no-margin">'
    return JsonResponse({'friends_html': friends_html, 'number_of_connected_friends': number_of_connected_friends, 'number_of_friends': number_of_friends})


@auth_required
def profile(request, mydata):
    return render(request, 'profile.html', {'mydata': mydata})


@auth_required
def messages(request, mydata):
    return render(request, 'messages.html', {'mydata': mydata})


@auth_required
def world(request, mydata):
    users_list = User.objects.exclude(id=mydata.id)
    for user in users_list:
        friend_request_list = User.objects.filter(id__in=Friend_Request.objects.filter(
            to_user_id=mydata.id).values('from_user_id')).order_by('name')
        friend_list = User.objects.filter(id__in=mydata.friends.through.objects.filter(
            from_user_id=mydata.id).values('to_user_id')).order_by('name')
    return render(request, 'world.html', {'mydata': mydata, 'users_list': users_list, 'friend_request_list': friend_request_list, 'friend_list': friend_list})


@auth_required
def send_friend_request(request, mydata, user_id):
    from_user = mydata
    to_user = User.objects.get(id=user_id)
    friend_request = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user)
    if friend_request:
        return JsonResponse({'send': True})
    else:
        return JsonResponse({'send': False})


@auth_required
def accept_friend_request(request, mydata, from_user_id):
    friend_request = Friend_Request.objects.get(
        from_user=from_user_id, to_user=mydata.id)
    if friend_request:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return JsonResponse({'friend': "accepted"})
    else:
        return JsonResponse({'error': True})


@auth_required
def reject_friend_request_received(request, mydata, from_user_id):
    friend_request = Friend_Request.objects.get(
        from_user=from_user_id, to_user=mydata.id)
    if friend_request:
        friend_request.delete()
        return JsonResponse({'friend': "rejected"})
    else:
        return JsonResponse({'error': True})


@auth_required
def reject_friend_request_sent(request, mydata, to_user_id):
    friend_request = Friend_Request.objects.get(
        from_user=mydata.id, to_user=to_user_id)
    if friend_request:
        friend_request.delete()
        return JsonResponse({'friend': "rejected"})
    else:
        return JsonResponse({'error': True})


@auth_required
def find_users(request, mydata, search_word):
    if request.is_ajax():
        friends = User.objects.filter(id__in=mydata.friends.through.objects.filter(
            from_user_id=mydata.id).values('to_user_id'))
        requests_sent = User.objects.filter(
            id__in=Friend_Request.objects.filter(from_user_id=mydata.id).values('to_user_id'))
        requests_received = User.objects.filter(
            id__in=Friend_Request.objects.filter(to_user_id=mydata.id).values('from_user_id'))
        users_found = User.objects.filter(
            Q(name__icontains=search_word) | Q(surnames__icontains=search_word)).exclude(id=mydata.id)
        users_found_html = '<div id="search-results" class="list">'
        if users_found:
            for user in users_found:
                if user.profile_pic:
                    users_found_html += '<div class="search-result"><img src="' + settings.MEDIA_URL + \
                        str(user.profile_pic) + '" class="small-profile-pic"> ' + '<p class="small text-centered">' + \
                        user.name + " " + user.surnames + '</p><div class="button-container">'
                else:
                    users_found_html += '<div class="search-result"><img src="' + static('images/default-user.png') + '" class="small-profile-pic"> ' + \
                        '<p class="small text-centered">' + user.name + " " + \
                        user.surnames + '</p><div class="button-container">'
                if user in friends:
                    users_found_html += '<p class="no-click-button right">Friend</p><br>'
                elif user in requests_sent:
                    users_found_html += '<a class="button right" href="#" data-requestsentid="' + \
                        str(user.id) + \
                        '" onclick="rejectFriendRequestSent(this)">Cancel request...</a><br>'
                elif user in requests_received:
                    users_found_html += '<a class="button" data-confirmid="' + \
                        str(user.id) + '" onclick="acceptFriend(this)" href="#">Confirm</a> <a class="button" data-rejectid="' + \
                        str(user.id) + \
                        '" onclick="rejectFriendRequestReceived(this)" href="#">Cancel</a>'
                else:
                    users_found_html += '<a class="button right" href="#" data-requesttosendid="' + \
                        str(user.id) + \
                        '" onclick="sendFriendRequest(this)">Send request</a><br>'
                users_found_html += '</div></div><hr style="clear:both;">'
            return HttpResponse(users_found_html)
        else:
            users_found_html += '<p>No results found containing "' + search_word + '"</p></div>'
            return HttpResponse(users_found_html)
    else:
        return redirect('/world/')


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


@auth_required
def upload_profile_pic(request, mydata):
    if request.is_ajax():
        if request.method == 'POST':
            form = ProfilePicUploadForm(request.POST, request.FILES)
            if form.is_valid():
                profile_pic = request.FILES.get('profile_pic')
                mydata.profile_pic = profile_pic
                mydata.save()
                return JsonResponse({'error': False, 'path': mydata.profile_pic.name})
            else:
                return JsonResponse({'error': True})
        else:
            return JsonResponse({'error': True})
    else:
        return redirect('/profile/')


@auth_required
def upload_photo(request, mydata):
    if request.is_ajax():
        if request.method == 'POST':
            form = PhotoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                photo = request.FILES.get('picture')
                myimage = Photo(profile=mydata,
                                picture=photo)
                myimage.save()
                return JsonResponse({'error': False, 'path': myimage.picture.name})
            else:
                return JsonResponse({'error': True})
        else:
            return JsonResponse({'error': True})
    else:
        return redirect('/profile/')


@auth_required
def get_my_photos(request, mydata):
    if request.is_ajax():
        if request.method == 'GET':
            my_photos = Photo.objects.filter(profile=mydata.id)
            html = ""
            for photo in my_photos:
                html += '<div class="col-lg-3 col-md-4 col-6"><div class="d-block mb-4 h-100"><a href="#"><img class="img-fluid image" src="' + settings.MEDIA_URL + \
                    str(photo.picture) + '" alt="' + str(photo.picture.name) + \
                    '"></a></div></div>'
            return HttpResponse(html)
        else:
            return JsonResponse({'error': True})
    else:
        return redirect('/profile/')


@auth_required
def logout(request, mydata):
    response = render(request, 'main.html')
    response.delete_cookie('auth_token')
    return response
