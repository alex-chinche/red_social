from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.register, name='login'),
    path('confirm_mail/<str:token>', views.confirm_email),
    path('main', views.main, name='main'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
