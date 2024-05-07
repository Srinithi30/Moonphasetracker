from django.db import models

# Create your models here.
# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def _str_(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add additional fields here if needed, such as name, date of birth, etc.
    # Example:
    # name = models.CharField(max_length=100)
    # date_of_birth = models.DateField()

    def _str_(self):
        return self.user.email
    
    
    # models.py

from django.db import models

from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notification_time = models.TimeField(null=True, blank=True)
    cycle_length = models.PositiveIntegerField(null=True, blank=True)
    period_length = models.PositiveIntegerField(null=True, blank=True)
    PERIOD_REMINDER_CHOICES = [
        ('none', 'None'),
        ('day-before', 'Day Before'),
        ('two-days-before', 'Two Days Before'),
    ]
    period_reminder = models.CharField(max_length=15, choices=PERIOD_REMINDER_CHOICES, default='none')
    PREGNANCY_STATUS_CHOICES = [
        ('no', 'No'),
        ('yes', 'Yes'),
    ]
    pregnant = models.CharField(max_length=3, choices=PREGNANCY_STATUS_CHOICES, default='no')

    def str(self):
        return f"{self.user.username}'s Settings"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField()

    def str(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):
        total = sum(product.price for product in self.products.all())
        self.total_price = total
        self.save()

    def str(self):
        return f"Cart for {self.user.username}"


class Symptom(models.Model):
    name = models.CharField(max_length=200)

    def str(self):
        return self.name


class PeriodNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period_starts_today = models.BooleanField(default=False)
    period_ends_today = models.BooleanField(default=False)
    drink_water = models.BooleanField(default=False)
    symptoms = models.ManyToManyField(Symptom)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Period Notes for {self.user.username}"


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Reminder for {self.user.username}"
    

from django.db import models
from django.contrib.auth.models import User

class Period(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Diet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    activity = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()

class CalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()



class Exercise1(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def str(self):
        return self.name

class DietPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def str(self):
        return self.name

