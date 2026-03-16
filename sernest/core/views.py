from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, ServiceProvider, User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .google_sheet import save_contact


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
        return redirect('home')

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

        try:
            save_contact(name, email, subject, message)

            send_mail(
                subject=f'Thanks for contacting SerNest',
                message=f"""Hi {name},

Thank you for contacting SerNest.

We received your message:
"{message}"

Our team will respond shortly.

Best regards,
SerNest Team""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, '✅ Your message was sent successfully!')

        except Exception as e:
            print(e)
            messages.error(request, '❌ Message failed to send. Please try again.')

    return render(request, 'contact.html')