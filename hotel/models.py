from django.db import models
from  user.models import  User
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

# Create your models here.

class Hotel(models.Model):
    hotel_name = models.CharField(
        'hotelName', blank=False, max_length=15, null=False, validators=[MinLengthValidator(3)])
    hotel_desc = models.CharField(
        'hotelDescription', blank=False, max_length=150, null=False, validators=[MinLengthValidator(3)])
    # origin = CountryField(null=False, blank=False)

    room_price = models.PositiveIntegerField('roomPrice', blank=False, null=False, validators=[
                                               MinValueValidator(15), MaxValueValidator(7000)])
    available_rooms = models.IntegerField(
        'availableRooms', blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(70)])
    longitude = models.CharField('longitude', blank=False, max_length=15, null=False, validators=[MinLengthValidator(3)])
    latitude = models.CharField('longitude', blank=False, max_length=15, null=False, validators=[MinLengthValidator(3)])

    def __str__(self):
        return f'{self.hotel_name}:{self.hotel_desc}'
