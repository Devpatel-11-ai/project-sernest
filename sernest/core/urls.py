from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
  path('signup/', views.UserSignupView, name='signup'),
  path('login/', views.UserLoginView, name='login'),
  path('', views.home, name='home'),
  path('categories/', views.categories, name="categories"),
  path('category/<int:id>/', views.category_providers, name='category_providers'),
  path('provider_register/', views.provider_register, name='provider_register'),
  path("search/", views.search_categories, name="search_categories"),
  path('logout/', views.UserLogoutView, name='logout'),
  path('register/',views.register,name='register'),

 # ── NEW: Dashboards ──
  path('dashboard/',views.user_dashboard,name='user_dashboard'),
  path('dashboard/provider/',views.provider_dashboard,name='provider_dashboard'),
  path('dashboard/admin/',views.admin_dashboard,name='admin_dashboard'),
 
 # ── NEW: Profiles ──
  path('profile/',views.user_profile,name='user_profile'),
  path('profile/provider/',views.provider_profile,name='provider_profile'),
 
 # ── NEW: Role redirect after login ──
  path('redirect/',views.role_redirect,name='role_redirect'),
  
]
