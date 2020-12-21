from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('confirm/<str:token>', views.confirm_email),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
