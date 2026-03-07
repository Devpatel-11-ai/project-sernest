from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
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

# Create your models here.
class User(AbstractBaseUser):

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    email = models.EmailField(unique=True)
    role_choice = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('service provider', 'Service Provider'),
        ('payment manager', 'Payment Manager'),
    )
    role = models.CharField(max_length=20, choices=role_choice,default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    # override username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

class Category(models.Model):

    SERVICE_GROUPS = [
        ('home', 'Home & Local Services'),
        ('professional', 'Professional & Freelance Services'),
        ('skilled', 'Local Skilled Workers'),
    ]

    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)
    group = models.CharField(max_length=100, choices=SERVICE_GROUPS)

    def __str__(self):
        return self.name

class ServiceProvider(models.Model):

    WORK_TYPE = [
        ('local', 'Local Service Worker'),
        ('freelancer', 'Freelancer'),
        ('company', 'Company'),
    ]

    MODE = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('both', 'Both'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    city = models.CharField(max_length=100)

    experience = models.IntegerField()

    rating = models.FloatField(default=4.5)

    work_type = models.CharField(max_length=20, choices=WORK_TYPE)

    mode = models.CharField(max_length=20, choices=MODE)

    available = models.BooleanField(default=True)

    profile_image = models.ImageField(upload_to="providers/")

    def __str__(self):
        return self.name