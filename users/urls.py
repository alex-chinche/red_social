from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ############### Public section ###################
    path('', views.main, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('confirm/<str:token>', views.confirm_email),
    ############### Private section ###################
    path('home/', views.home, name='home'),
    path('pulse/', views.send_pulse, name='send_pulse'),
    # Profile section
    path('profile/', views.profile, name='profile'),
    path('upload_profile_pic/',
         views.upload_profile_pic, name='upload_profile_pic'),
    path('upload_photo/',
         views.upload_photo, name='upload_photo'),
    path('get_my_photos/',
         views.get_my_photos, name='get_my_photos'),

    # Messages section
    path('messages/', views.messages, name='messages'),
    # World section
    path('world/', views.world, name='world'),
    path('send_friend_request/<int:user_id>/',
         views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:from_user_id>/',
         views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request_sent/<int:to_user_id>/',
         views.reject_friend_request_sent, name='reject_friend_request_sent'),
    path('reject_friend_request_received/<int:from_user_id>/',
         views.reject_friend_request_received, name='reject_friend_request_received'),
    path('find_users/<str:search_word>/',
         views.find_users, name='find_users'),
    path('get_friend_list/',
         views.get_friend_list, name='get_friend_list'),
    # Logout
    path('logout/',
         views.logout, name='logout'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
