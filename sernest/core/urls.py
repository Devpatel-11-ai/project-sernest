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
  
 
 # ── NEW: Profiles ──
  path('profile/',views.user_profile,name='user_profile'),
  path('profile/provider/',views.provider_profile,name='provider_profile'),
 
 # ── NEW: Role redirect after login ──
  path('redirect/',views.role_redirect,name='role_redirect'),

  # ══════════════════════════════════════════════════════════════
  #  ADD THESE LINES to your core/urls.py  urlpatterns list
  #  (after the existing dashboard lines)
  # ══════════════════════════════════════════════════════════════
   
 # --- Admin management URLs ---
  path('dashboard/admin/',          views.admin_dashboard,        name='admin_dashboard'),
  path('dashboard/admin/users/',    views.admin_users,            name='admin_users'),
  path('dashboard/admin/users/<int:user_id>/toggle/', views.admin_toggle_user, name='admin_toggle_user'),
  path('dashboard/admin/providers/',views.admin_providers,        name='admin_providers'),
  path('dashboard/admin/providers/<int:provider_id>/toggle/', views.admin_toggle_provider, name='admin_toggle_provider'),
  path('dashboard/admin/bookings/', views.admin_bookings,         name='admin_bookings'),
  path('dashboard/admin/bookings/<int:booking_id>/edit/',   views.admin_booking_edit,   name='admin_booking_edit'),
  path('dashboard/admin/bookings/<int:booking_id>/delete/', views.admin_booking_delete, name='admin_booking_delete'),
  

  # ══════════════════════════════════════════════════════════════
  #  ADD THESE LINES to core/urls.py urlpatterns list
  # ══════════════════════════════════════════════════════════════
  
  # --- Booking URLs ---
  path('booking/create/',                          views.create_booking,             name='create_booking'),
  path('booking/slots/',                           views.get_slot_availability,      name='slot_availability'),
  path('booking/<int:booking_id>/accept/',         views.provider_accept_booking,    name='provider_accept_booking'),
  path('booking/<int:booking_id>/reject/',         views.provider_reject_booking,    name='provider_reject_booking'),
  path('booking/<int:booking_id>/complete/',       views.provider_complete_booking,  name='provider_complete_booking'),
  path('booking/<int:booking_id>/cancel/',         views.user_cancel_booking,        name='user_cancel_booking'),
 
  ]
