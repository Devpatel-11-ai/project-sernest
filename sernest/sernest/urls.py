"""
URL configuration for sernest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from django.conf import settings
from core import views as core_views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('categories/', views.categories, name='categories'),
    path('about/', views.about, name='about'),
    path('contact/', core_views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('provider_register/', views.provider_register, name='provider_register'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
    template_name='registration/password_reset.html',
    email_template_name='registration/password_reset_email.txt',
    success_url='/password-reset/sent/'
    ), name='password_reset'),
    
    path('password-reset/sent/', auth_views.PasswordResetDoneView.as_view(
    template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='registration/password_reset_confirm.html',
    success_url='/password-reset/complete/'
    ), name='password_reset_confirm'),
    
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
    template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    
    # path("test/",views.test),
  
  
    #http://127.0.0.1/:8000/recap

    #app level url config

   
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
