from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator , MinLengthValidator
from django_countries.fields import CountryField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('dob', '1997-5-5')
        extra_fields.setdefault('zip_code', '15289')
        extra_fields.setdefault('city', 'Cairo')
        extra_fields.setdefault('country', 'EG')
        extra_fields.setdefault('street_name', '14m')

        return self.create_user(username, password, **extra_fields)
    
    def normalize_username(self, username):
        """
        Normalize the username by lowercasing it.
        """
        return username.lower()
    

class User(AbstractBaseUser):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ]
    first_name = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    last_name = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    phone_regex = RegexValidator(regex=r'^\d{1,20}$', message="Phone number should contain only digits.")
    username = models.CharField(max_length=255, null=False, blank=False ,unique=True)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=False, blank=False)
    image = models.FileField(upload_to='user_images', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True, validators=[phone_regex])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False, blank=False )
    zip_code = models.CharField(max_length=20, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    country = CountryField(null=False, blank=False)
    street_name = models.CharField(null=False, max_length=255)
    building_no =models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'gender']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_module_perms(self, app_label):
        # return True if the user has any permissions for the given app label
        return self.is_active and self.is_staff

    def has_perm(self, perm, obj=None):
        # return True if the user has the specified permission
        return self.is_active and self.is_superuser
    
