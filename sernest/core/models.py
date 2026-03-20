# ══════════════════════════════════════════════════════════════
#  COMPLETE core/models.py  — replace your entire models.py
# ══════════════════════════════════════════════════════════════

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    def has_perm(self, perm, obj=None): return self.is_admin
    def has_module_perms(self, app_label): return self.is_admin

    email        = models.EmailField(unique=True)
    first_name   = models.CharField(max_length=50,  blank=True, default='')
    last_name    = models.CharField(max_length=50,  blank=True, default='')
    phone        = models.CharField(max_length=15,  blank=True, default='')
    city         = models.CharField(max_length=100, blank=True, default='')
    address      = models.CharField(max_length=255, blank=True, default='')
    postal_code  = models.CharField(max_length=10,  blank=True, default='')
    state        = models.CharField(max_length=100, blank=True, default='')
    landmark     = models.CharField(max_length=255, blank=True, default='')
    profile_photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    role_choice = (
        ('admin',            'Admin'),
        ('user',             'User'),
        ('service provider', 'Service Provider'),
        ('payment manager',  'Payment Manager'),
    )
    role       = models.CharField(max_length=20, choices=role_choice, default='user')
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    is_admin   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Category(models.Model):
    SERVICE_GROUPS = [
        ('home',         'Home & Local Services'),
        ('professional', 'Professional & Freelance Services'),
        ('skilled',      'Local Skilled Workers'),
    ]
    name  = models.CharField(max_length=100)
    icon  = models.CharField(max_length=10)
    group = models.CharField(max_length=100, choices=SERVICE_GROUPS)

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    WORK_TYPE = [
        ('local',      'Local Service Worker'),
        ('freelancer', 'Freelancer'),
        ('company',    'Company'),
    ]
    MODE = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('both',   'Both'),
    ]

    name     = models.CharField(max_length=100)
    phone    = models.CharField(max_length=15)
    email    = models.EmailField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city     = models.CharField(max_length=100)
    experience = models.IntegerField()
    rating   = models.FloatField(default=4.5)
    work_type = models.CharField(max_length=20, choices=WORK_TYPE)
    mode     = models.CharField(max_length=20, choices=MODE)
    available = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='providers/', blank=True, null=True)

    def __str__(self):
        return self.name


# ══════════════════════════════════════════════════════════════
#  NEW: TimeSlot — tracks availability per provider per date
# ══════════════════════════════════════════════════════════════
class TimeSlot(models.Model):
    SLOT_CHOICES = [
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
    MAX_BOOKINGS = 5  # max bookings per slot per provider

    provider    = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='time_slots')
    date        = models.DateField()
    slot_time   = models.CharField(max_length=10, choices=SLOT_CHOICES)
    booked_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('provider', 'date', 'slot_time')
        ordering = ['date', 'slot_time']

    def __str__(self):
        return f"{self.provider.name} | {self.date} | {self.slot_time} ({self.booked_count}/{self.MAX_BOOKINGS})"

    @property
    def is_full(self):
        return self.booked_count >= self.MAX_BOOKINGS

    @property
    def slots_left(self):
        return max(0, self.MAX_BOOKINGS - self.booked_count)


# ══════════════════════════════════════════════════════════════
#  UPDATED: Booking model — with slot, pricing, and status flow
# ══════════════════════════════════════════════════════════════
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('accepted',    'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
        ('cancelled',   'Cancelled'),
        ('rejected',    'Rejected'),
    ]

    user     = models.ForeignKey(User,            on_delete=models.CASCADE,   related_name='bookings')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL,  related_name='bookings', null=True, blank=True)
    category = models.ForeignKey(Category,        on_delete=models.SET_NULL,  null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot,       on_delete=models.SET_NULL,  null=True, blank=True, related_name='bookings')

    service_name   = models.CharField(max_length=200)
    description    = models.TextField(blank=True, default='')
    address        = models.CharField(max_length=300, blank=True, default='')
    city           = models.CharField(max_length=100, blank=True, default='')
    phone          = models.CharField(max_length=15, blank=True, default='')
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.CharField(max_length=10, blank=True, default='')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Pricing fields — filled when provider accepts
    estimate_amount  = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # provider's estimate
    company_margin   = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 5% of estimate
    gst_amount       = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 18% of (estimate + margin)
    total_amount     = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # final total
    payment_method   = models.CharField(max_length=20, blank=True, default='cash')

    notes            = models.TextField(blank=True, default='')
    provider_notes   = models.TextField(blank=True, default='')  # provider's message on accept/reject

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} – {self.service_name} ({self.status})"

    def calculate_pricing(self, estimate):
        """Calculate and save pricing breakdown"""
        from decimal import Decimal
        estimate = Decimal(str(estimate))
        margin   = round(estimate * Decimal('0.05'), 2)       # 5% company margin
        subtotal = estimate + margin
        gst      = round(subtotal * Decimal('0.18'), 2)       # 18% GST
        total    = subtotal + gst

        self.estimate_amount = estimate
        self.company_margin  = margin
        self.gst_amount      = gst
        self.total_amount    = total
        return total

    class Meta:
        ordering = ['-created_at']