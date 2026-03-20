from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, ServiceProvider, User
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.core.mail import send_mail
from django.conf import settings
from .google_sheet import save_contact
from django.utils import timezone
from datetime import timedelta
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator






# ══════════════════════════════════════
#  REGISTER (User signup)
# ══════════════════════════════════════
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name  = request.POST.get('first_name', '').strip()
        last_name   = request.POST.get('last_name', '').strip()
        email       = request.POST.get('email', '').strip().lower()
        phone       = request.POST.get('phone', '').strip()
        city        = request.POST.get('city', '').strip()
        password    = request.POST.get('password', '')

        # Validation
        if not all([first_name, email, password]):
            messages.error(request, '❌ Please fill in all required fields.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ An account with this email already exists.')
            return render(request, 'register.html')

        if len(password) < 6:
            messages.error(request, '❌ Password must be at least 6 characters.')
            return render(request, 'register.html')

        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
        )
        user.first_name = first_name
        user.last_name  = last_name
        # Store phone/city in a profile or just skip if not on User model
        user.save()

        messages.success(request, '✅ Account created! Please sign in.')
        return redirect('login')

    return render(request, 'register.html')


# ══════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════
def UserLoginView(request):
    if request.user.is_authenticated:
        return redirect('core:role_redirect')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, '❌ Please enter both email and password.')
            return render(request, 'core/login.html')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'✅ Welcome back!')

                # Redirect based on role
                if user.role == 'admin':
                    return redirect('admin:index')
                else:
                    # Go to next page if specified, else home
                    next_url = request.GET.get('next', '')
                    return redirect(next_url if next_url else 'home')
            else:
                messages.error(request, '❌ Your account is inactive. Contact support.')
        else:
            messages.error(request, '❌ Invalid email or password. Please try again.')

    return render(request, 'core/login.html')


# ══════════════════════════════════════
#  LOGOUT
# ══════════════════════════════════════
def UserLogoutView(request):
    logout(request)
    messages.success(request, '✅ You have been signed out.')
    return redirect('home')


# ══════════════════════════════════════
#  USER SIGNUP (same as register, kept for URL compatibility)
# ══════════════════════════════════════
def UserSignupView(request):
    return register(request)


# ══════════════════════════════════════
#  HOME
# ══════════════════════════════════════
def home(request):
    return render(request, 'home.html')


# ══════════════════════════════════════
#  PROVIDER REGISTER
# ══════════════════════════════════════
def provider_register(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name        = request.POST.get('provider_name', '').strip()
        phone       = request.POST.get('phone', '').strip()
        email       = request.POST.get('email', '').strip().lower()
        category_id = request.POST.get('category', '')
        city        = request.POST.get('service_area', '').strip()
        experience  = request.POST.get('experience', 0)
        work_type   = request.POST.get('work_type', 'local')
        mode        = request.POST.get('mode', 'onsite')
        password    = request.POST.get('password', '')

        # Validation
        if not all([name, phone, email, category_id, city, password]):
            messages.error(request, '❌ Please fill in all required fields.')
            return render(request, 'provider_register.html', {'categories': categories})

        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ An account with this email already exists.')
            return render(request, 'provider_register.html', {'categories': categories})

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, '❌ Invalid category selected.')
            return render(request, 'provider_register.html', {'categories': categories})

        # Create User account for provider
        user = User.objects.create_user(
            email=email,
            password=password,
        )
        user.first_name = name
        user.role = 'service provider'
        user.save()

        # Create ServiceProvider profile
        ServiceProvider.objects.create(
            name=name,
            phone=phone,
            email=email,
            category=category,
            city=city,
            experience=int(experience) if experience else 0,
            work_type=work_type,
            mode=mode,
        )

        messages.success(
            request,
            '✅ Application submitted! Our team will review your profile within 24 hours.'
        )
        return redirect('login')

    return render(request, 'provider_register.html', {'categories': categories})


# ══════════════════════════════════════
#  CATEGORIES
# ══════════════════════════════════════
def categories(request):
    home_services        = Category.objects.filter(group='home')
    professional_services = Category.objects.filter(group='professional')
    skilled_services     = Category.objects.filter(group='skilled')

    return render(request, 'categories.html', {
        'home_services':         home_services,
        'professional_services': professional_services,
        'skilled_services':      skilled_services,
    })


# ══════════════════════════════════════
#  CATEGORY PROVIDERS
# ══════════════════════════════════════
def category_providers(request, id):
    category       = Category.objects.get(id=id)
    providers      = ServiceProvider.objects.filter(category=category)
    all_categories = Category.objects.all()

    return render(request, 'category_providers.html', {
        'category':       category,
        'providers':      providers,
        'all_categories': all_categories,
    })


# ══════════════════════════════════════
#  SEARCH CATEGORIES (AJAX)
# ══════════════════════════════════════
def search_categories(request):
    query   = request.GET.get('q', '').strip()
    results = []

    if query:
        cats = Category.objects.filter(name__icontains=query)[:8]
        for cat in cats:
            results.append({
                'id':   cat.id,
                'name': cat.name,
                'icon': cat.icon,
            })

    return JsonResponse(results, safe=False)


# ══════════════════════════════════════
#  ABOUT
# ══════════════════════════════════════
def about(request):
    return render(request, 'about.html')


# ══════════════════════════════════════
#  CONTACT
# ══════════════════════════════════════
def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        date    = datetime.now().strftime('%d-%m-%Y %H:%M')

        if not all([name, email, subject, message]):
            messages.error(request, '❌ Please fill in all fields.')
            return render(request, 'contact.html')

        # ✅ Google Sheet
        try:
            save_contact(name, email, subject, message)
            print("✅ Sheet saved!")
        except Exception as e:
            import traceback
            print("❌ SHEET ERROR:", traceback.format_exc())

        # ✅ Email to user
        try:
            send_mail(
                subject=f'We received your message — {subject}',
                message=f"""Hi {name},

Thank you for contacting SerNest! We received your message.

Subject : {subject}
Message : {message}
Date    : {date}

Best regards,
SerNest Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            print("✅ User email sent!")
        except Exception as e:
            import traceback
            print("❌ EMAIL ERROR:", traceback.format_exc())

        # ✅ Email to admin
        try:
            send_mail(
                subject=f'New Contact: {subject}',
                message=f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}\nDate: {date}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print("✅ Admin email sent!")
        except Exception as e:
            import traceback
            print("❌ ADMIN EMAIL ERROR:", traceback.format_exc())

        messages.success(request, f'✅ Thank you {name}! Message sent successfully.')
        return redirect('contact')

    return render(request, 'contact.html')


# ═══════════════════════════════════════════════════════
#  ADD THESE FUNCTIONS TO YOUR EXISTING core/views.py
#  Also add:  from django.contrib.auth.decorators import login_required
# ═══════════════════════════════════════════════════════

from django.contrib.auth.decorators import login_required

# ──────────────────────────────────────────
#  USER PROFILE
# ──────────────────────────────────────────
@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name  = request.POST.get('first_name', '')
        user.last_name   = request.POST.get('last_name', '')
        user.phone       = request.POST.get('phone', '')
        user.city        = request.POST.get('city', '')
        user.address     = request.POST.get('address', '')
        user.postal_code = request.POST.get('postal_code', '')
        user.state       = request.POST.get('state', '')
        user.landmark    = request.POST.get('landmark', '')

        # Handle profile photo upload
        if request.POST.get('remove_photo') == '1':
            if user.profile_photo:
                 user.profile_photo.delete(save=False)
            user.profile_photo = None
        elif 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']

        user.save()
        messages.success(request, '✅ Profile updated successfully!')
        return redirect('core:user_profile')

    return render(request, 'profiles/user_profile.html', {'user': request.user})


# ──────────────────────────────────────────
#  PROVIDER PROFILE
# ──────────────────────────────────────────
@login_required
def provider_profile(request):
    from .models import ServiceProvider, Category

    try:
        provider = ServiceProvider.objects.get(email=request.user.email)
    except ServiceProvider.DoesNotExist:
        provider = None

    categories = Category.objects.all()

    if request.method == 'POST' and provider:
        provider.name       = request.POST.get('name', provider.name)
        provider.city       = request.POST.get('city', provider.city)
        provider.experience = request.POST.get('experience', provider.experience)
        provider.mode       = request.POST.get('mode', provider.mode)
        provider.available  = request.POST.get('available') == 'on'
        if request.POST.get('remove_photo') == '1':
            if provider.profile_image:
                provider.profile_image.delete(save=False)
            provider.profile_image = None
        elif 'profile_image' in request.FILES:
            provider.profile_image = request.FILES['profile_image']
        provider.save()
        from django.contrib import messages
        messages.success(request, '✅ Profile updated successfully!')
        return redirect('core:provider_profile')

    return render(request, 'profiles/provider_profile.html', {
    'provider':   provider,
    'categories': categories,
    'days_list':  ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'rating_levels': ['5', '4', '3', '2', '1'],
})


# ──────────────────────────────────────────
#  REDIRECT AFTER LOGIN (based on role)
# ──────────────────────────────────────────
def role_redirect(request):
    if not request.user.is_authenticated:
        return redirect('core:login')
    role = request.user.role
    if role == 'admin':
        return redirect('core:admin_dashboard')
    elif role == 'service provider':
        return redirect('core:provider_dashboard')
    else:
        return redirect('core:user_dashboard')

def admin_required(view_func):
    """Decorator: only allow users with role='admin'"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
 
 
# ──────────────────────────────────────────
#  ADMIN DASHBOARD  (main overview)
# ──────────────────────────────────────────
@login_required
@admin_required
def admin_dashboard(request):
    from .models import User, ServiceProvider, Booking
 
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
 
    # Stats
    total_users     = User.objects.filter(role='user').count()
    total_providers = ServiceProvider.objects.count()
    total_bookings  = Booking.objects.count()
    total_revenue = Booking.objects.filter(status='completed').aggregate(t=Sum('total_amount'))['t'] or 0
    pending_bookings = Booking.objects.filter(status='pending').count()
    active_providers = ServiceProvider.objects.filter(available=True).count()
 
    # Recent data
    recent_bookings  = Booking.objects.select_related('user','provider','category').order_by('-created_at')[:8]
    recent_users     = User.objects.filter(role='user').order_by('-created_at')[:5]
    recent_providers = ServiceProvider.objects.select_related('category').order_by('-id')[:5]
 
    # Weekly revenue chart
    weekly_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        rev = Booking.objects.filter(
            status='completed',
            updated_at__date=day
        ).aggregate(t=Sum('total_amount'))['t'] or 0
        weekly_data.append({'day': day.strftime('%a'), 'revenue': float(rev)})
 
    context = {
        'total_users':       total_users,
        'total_providers':   total_providers,
        'total_bookings':    total_bookings,
        'total_revenue':     total_revenue,
        'pending_bookings':  pending_bookings,
        'active_providers':  active_providers,
        'recent_bookings':   recent_bookings,
        'recent_users':      recent_users,
        'recent_providers':  recent_providers,
        'weekly_data':       weekly_data,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)
 
 
# ──────────────────────────────────────────
#  MANAGE USERS
# ──────────────────────────────────────────
@login_required
@admin_required
def admin_users(request):
    from .models import User
    query = request.GET.get('q', '')
    users = User.objects.filter(role='user').order_by('-created_at')
    if query:
        users = users.filter(Q(first_name__icontains=query) | Q(email__icontains=query))
    return render(request, 'dashboards/admin_users.html', {'users': users, 'query': query})
 
 
@login_required
@admin_required
def admin_toggle_user(request, user_id):
    from .models import User
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'✅ User {user.email} has been {status}.')
    return redirect('core:admin_users')
 
 
# ──────────────────────────────────────────
#  MANAGE SERVICE PROVIDERS
# ──────────────────────────────────────────
@login_required
@admin_required
def admin_providers(request):
    from .models import ServiceProvider
    query = request.GET.get('q', '')
    providers = ServiceProvider.objects.select_related('category').order_by('-id')
    if query:
        providers = providers.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(city__icontains=query))
    return render(request, 'dashboards/admin_providers.html', {'providers': providers, 'query': query})
 
 
@login_required
@admin_required
def admin_toggle_provider(request, provider_id):
    from .models import ServiceProvider
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    provider.available = not provider.available
    provider.save()
    status = 'activated' if provider.available else 'deactivated'
    messages.success(request, f'✅ Provider {provider.name} has been {status}.')
    return redirect('core:admin_providers')
 
 
# ──────────────────────────────────────────
#  MANAGE BOOKINGS
# ──────────────────────────────────────────
@login_required
@admin_required
def admin_bookings(request):
    from .models import Booking
    query  = request.GET.get('q', '')
    status = request.GET.get('status', '')
    bookings = Booking.objects.select_related(
        'user', 'provider', 'category'
    ).order_by('-created_at')
 
    if query:
        bookings = bookings.filter(
            Q(service_name__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__email__icontains=query)
        )
    if status:
        bookings = bookings.filter(status=status)
 
    return render(request, 'dashboards/admin_bookings.html', {
        'bookings': bookings,
        'query': query,
        'status_filter': status,
        'status_choices': [
            ('pending',     'Pending'),
            ('accepted',    'Accepted'),
            ('in_progress', 'In Progress'),
            ('completed',   'Completed'),
            ('cancelled',   'Cancelled'),
            ('rejected',    'Rejected'),
        ],
    })
 
 
@login_required
@admin_required
def admin_booking_edit(request, booking_id):
    from .models import Booking, ServiceProvider
    booking   = get_object_or_404(Booking, id=booking_id)
    providers = ServiceProvider.objects.all()
 
    if request.method == 'POST':
        booking.service_name   = request.POST.get('service_name', booking.service_name)
        booking.status         = request.POST.get('status', booking.status)
        booking.address        = request.POST.get('address', booking.address)
        booking.city           = request.POST.get('city', booking.city)
        booking.scheduled_date = request.POST.get('scheduled_date') or None
        booking.scheduled_time = request.POST.get('scheduled_time') or ''
        booking.notes          = request.POST.get('notes', booking.notes)
 
        # Handle estimate — recalculate pricing
        estimate = request.POST.get('estimate_amount')
        if estimate:
            try:
                booking.calculate_pricing(float(estimate))
            except Exception:
                pass
 
        provider_id = request.POST.get('provider')
        if provider_id:
            booking.provider = get_object_or_404(ServiceProvider, id=provider_id)
        booking.save()
        messages.success(request, f'✅ Booking #{booking.id} updated successfully.')
        return redirect('core:admin_bookings')
 
    return render(request, 'dashboards/admin_booking_edit.html', {
        'booking':  booking,
        'providers': providers,
        'status_choices': [
            ('pending',     'Pending'),
            ('accepted',    'Accepted'),
            ('in_progress', 'In Progress'),
            ('completed',   'Completed'),
            ('cancelled',   'Cancelled'),
            ('rejected',    'Rejected'),
        ],
    })
 
 
 
@login_required
@admin_required
def admin_booking_delete(request, booking_id):
    from .models import Booking
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, f'✅ Booking #{booking_id} deleted.')
    return redirect('core:admin_bookings')
 

def get_slot_availability(request):
    """
    AJAX endpoint — returns slot status for a provider on a date.
    GET params: provider_id, date (YYYY-MM-DD)
    """
    from .models import TimeSlot, ServiceProvider
 
    provider_id = request.GET.get('provider_id')
    date        = request.GET.get('date')
 
    if not provider_id or not date:
        return JsonResponse({'error': 'Missing params'}, status=400)
 
    try:
        provider = ServiceProvider.objects.get(id=provider_id)
    except ServiceProvider.DoesNotExist:
        return JsonResponse({'error': 'Provider not found'}, status=404)
 
    ALL_SLOTS = [
        ('09:00', '9–10 AM'),
        ('10:00', '10–11 AM'),
        ('11:00', '11 AM–12 PM'),
        ('12:00', '12–1 PM'),
        ('13:00', '1–2 PM'),
        ('14:00', '2–3 PM'),
        ('15:00', '3–4 PM'),
        ('16:00', '4–5 PM'),
        ('17:00', '5–6 PM'),
    ]
 
    # Fetch existing slot records for this provider/date
    existing = {
        ts.slot_time: ts
        for ts in TimeSlot.objects.filter(provider=provider, date=date)
    }
 
    slots = []
    for slot_value, slot_label in ALL_SLOTS:
        ts = existing.get(slot_value)
        booked = ts.booked_count if ts else 0
        slots.append({
            'value':       slot_value,
            'label':       slot_label,
            'booked':      booked,
            'max':         TimeSlot.MAX_BOOKINGS,
            'available':   booked < TimeSlot.MAX_BOOKINGS,
            'slots_left':  TimeSlot.MAX_BOOKINGS - booked,
        })
 
    return JsonResponse({'slots': slots, 'provider': provider.name, 'date': date})
 
 
# ──────────────────────────────────────────────────────────────
#  CREATE BOOKING (User submits booking form)
# ──────────────────────────────────────────────────────────────
@login_required
def create_booking(request):
    if request.method != 'POST':
        return redirect('categories')
 
    from .models import ServiceProvider, Category, Booking, TimeSlot
 
    provider_id    = request.POST.get('provider_id')
    category_id    = request.POST.get('category_id')
    scheduled_date = request.POST.get('date')
    scheduled_time = request.POST.get('slot_time')
    full_name      = request.POST.get('full_name', '').strip()
    phone          = request.POST.get('phone', '').strip()
    address        = request.POST.get('address', '').strip()
    city           = request.POST.get('city', '').strip()
    description    = request.POST.get('description', '').strip()
    payment_method = request.POST.get('payment_method', 'cash')
 
    # Validate required fields
    if not all([provider_id, scheduled_date, scheduled_time]):
        messages.error(request, '❌ Please fill all required fields.')
        return redirect(request.META.get('HTTP_REFERER', 'categories'))
 
    try:
        provider = ServiceProvider.objects.get(id=provider_id)
        category = Category.objects.get(id=category_id) if category_id else provider.category
    except (ServiceProvider.DoesNotExist, Category.DoesNotExist):
        messages.error(request, '❌ Invalid provider or category.')
        return redirect('categories')
 
    # Check slot availability (max 5 per slot)
    slot, created = TimeSlot.objects.get_or_create(
        provider=provider,
        date=scheduled_date,
        slot_time=scheduled_time,
        defaults={'booked_count': 0}
    )
 
    if slot.is_full:
        messages.error(request, f'❌ This time slot is fully booked (max {TimeSlot.MAX_BOOKINGS}). Please choose another slot.')
        return redirect(request.META.get('HTTP_REFERER', 'categories'))
 
    # Create the booking
    booking = Booking.objects.create(
        user           = request.user,
        provider       = provider,
        category       = category,
        time_slot      = slot,
        service_name   = category.name,
        description    = description,
        address        = address,
        city           = city,
        phone          = phone,
        scheduled_date = scheduled_date,
        scheduled_time = scheduled_time,
        payment_method = payment_method,
        status         = 'pending',
        notes          = f'Booked by: {full_name}',
    )
 
    # Increment slot counter
    slot.booked_count += 1
    slot.save()
 
    messages.success(request, f'✅ Booking #{booking.id} placed successfully! Waiting for provider to accept.')
    return redirect('core:user_dashboard')
 
 
# ──────────────────────────────────────────────────────────────
#  PROVIDER: Accept booking + set estimate
# ──────────────────────────────────────────────────────────────
@login_required
def provider_accept_booking(request, booking_id):
    from .models import Booking, ServiceProvider
 
    try:
        provider = ServiceProvider.objects.get(email=request.user.email)
    except ServiceProvider.DoesNotExist:
        messages.error(request, '❌ Provider profile not found.')
        return redirect('core:provider_dashboard')
 
    booking = get_object_or_404(Booking, id=booking_id, provider=provider)
 
    if request.method == 'POST':
        estimate       = request.POST.get('estimate', 0)
        provider_notes = request.POST.get('provider_notes', '').strip()
 
        try:
            estimate = float(estimate)
            if estimate <= 0:
                raise ValueError('Estimate must be positive')
        except (ValueError, TypeError):
            messages.error(request, '❌ Please enter a valid estimate amount.')
            return redirect('core:provider_dashboard')
 
        # Calculate pricing
        booking.calculate_pricing(estimate)
        booking.provider_notes = provider_notes
        booking.status         = 'accepted'
        booking.save()
 
        messages.success(request, f'✅ Booking #{booking.id} accepted. Total: ₹{booking.total_amount}')
        return redirect('core:provider_dashboard')
 
    # GET — show accept form
    return render(request, 'bookings/provider_accept.html', {'booking': booking})
 
 
# ──────────────────────────────────────────────────────────────
#  PROVIDER: Reject booking
# ──────────────────────────────────────────────────────────────
@login_required
def provider_reject_booking(request, booking_id):
    from .models import Booking, ServiceProvider, TimeSlot
 
    try:
        provider = ServiceProvider.objects.get(email=request.user.email)
    except ServiceProvider.DoesNotExist:
        messages.error(request, '❌ Provider profile not found.')
        return redirect('core:provider_dashboard')
 
    booking = get_object_or_404(Booking, id=booking_id, provider=provider)
 
    if request.method == 'POST':
        provider_notes = request.POST.get('provider_notes', '').strip()
        booking.provider_notes = provider_notes or 'Rejected by provider.'
        booking.status = 'rejected'
        booking.save()
 
        # Free up the slot
        if booking.time_slot:
            slot = booking.time_slot
            slot.booked_count = max(0, slot.booked_count - 1)
            slot.save()
 
        messages.success(request, f'✅ Booking #{booking.id} rejected.')
        return redirect('core:provider_dashboard')
 
    return render(request, 'bookings/provider_reject.html', {'booking': booking})
 
 
# ──────────────────────────────────────────────────────────────
#  PROVIDER: Mark booking as completed
# ──────────────────────────────────────────────────────────────
@login_required
def provider_complete_booking(request, booking_id):
    from .models import Booking, ServiceProvider
 
    try:
        provider = ServiceProvider.objects.get(email=request.user.email)
    except ServiceProvider.DoesNotExist:
        return redirect('core:provider_dashboard')
 
    booking = get_object_or_404(Booking, id=booking_id, provider=provider, status='accepted')
    booking.status = 'completed'
    booking.save()
    messages.success(request, f'✅ Booking #{booking.id} marked as completed.')
    return redirect('core:provider_dashboard')
 
 
# ──────────────────────────────────────────────────────────────
#  USER: Cancel booking
# ──────────────────────────────────────────────────────────────
@login_required
def user_cancel_booking(request, booking_id):
    from .models import Booking
 
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
 
    if booking.status in ('pending', 'accepted'):
        booking.status = 'cancelled'
        booking.save()
 
        # Free up slot
        if booking.time_slot:
            slot = booking.time_slot
            slot.booked_count = max(0, slot.booked_count - 1)
            slot.save()
 
        messages.success(request, f'✅ Booking #{booking.id} cancelled.')
    else:
        messages.error(request, '❌ This booking cannot be cancelled.')
 
    return redirect('core:user_dashboard')
 
 
# ──────────────────────────────────────────────────────────────
#  UPDATED: user_dashboard — with real booking data
# ──────────────────────────────────────────────────────────────
@login_required
def user_dashboard(request):
    from .models import Category, Booking
 
    bookings         = Booking.objects.filter(user=request.user).select_related('provider', 'category').order_by('-created_at')[:10]
    active_bookings  = Booking.objects.filter(user=request.user, status__in=['pending','accepted','in_progress']).count()
    completed_bookings = Booking.objects.filter(user=request.user, status='completed').count()
    quick_categories = Category.objects.all()[:8]
 
    context = {
        'active_bookings':    active_bookings,
        'completed_bookings': completed_bookings,
        'saved_providers':    0,
        'wallet_balance':     0,
        'bookings':           bookings,
        'favorite_providers': [],
        'quick_categories':   quick_categories,
    }
    return render(request, 'dashboards/user_dashboard.html', context)
 
 
# ──────────────────────────────────────────────────────────────
#  UPDATED: provider_dashboard — with real booking data
# ──────────────────────────────────────────────────────────────
@login_required
def provider_dashboard(request):
    from .models import ServiceProvider, Booking
    from django.db.models import Sum
    from django.utils import timezone
 
    try:
        provider = ServiceProvider.objects.get(email=request.user.email)
    except ServiceProvider.DoesNotExist:
        provider = None
 
    today            = timezone.now().date()
    pending_requests = Booking.objects.filter(provider=provider, status='pending').select_related('user', 'category').order_by('-created_at') if provider else []
    accepted_bookings = Booking.objects.filter(provider=provider, status='accepted').select_related('user', 'category') if provider else []
    todays_bookings  = Booking.objects.filter(provider=provider, scheduled_date=today).count() if provider else 0
    completed_jobs   = Booking.objects.filter(provider=provider, status='completed').count() if provider else 0
    total_earnings   = Booking.objects.filter(provider=provider, status='completed').aggregate(t=Sum('total_amount'))['t'] or 0
 
    context = {
        'provider':          provider,
        'todays_bookings':   todays_bookings,
        'pending_requests':  pending_requests,
        'accepted_bookings': accepted_bookings,
        'completed_jobs':    completed_jobs,
        'total_earnings':    total_earnings,
        'today_earnings':    0,
        'week_earnings':     0,
        'month_earnings':    0,
    }
    return render(request, 'dashboards/provider_dashboard.html', context)
 