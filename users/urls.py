from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('confirm/<str:token>', views.confirm_email),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('messages/', views.messages, name='messages'),
    path('world/', views.world, name='world'),
    path('send_friend_request/<int:user_id>/',
         views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:from_user_id>/',
         views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:from_user_id>/',
         views.reject_friend_request, name='reject_friend_request'),
    path('find_users/<str:search_word>/',
         views.find_users, name='find_users'),
    path('logout/',
         views.logout, name='logout'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
