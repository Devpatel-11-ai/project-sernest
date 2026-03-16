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
]
