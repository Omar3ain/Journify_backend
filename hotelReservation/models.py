from django.db import models
from user.models import User
from hotel.models import Hotel
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import uuid
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator



# Create your models here.

class StayReservation(models.Model):
    room_choice = [
    ('S', 'Single'),
    ('D', 'Double'),
    ]
    stay_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=None)
    numberOfRooms=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    numberOfPeople = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    startDate = models.DateField(auto_now_add=True)
    numberOfDays = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=7, decimal_places=2, default=20)
    room_type = models.CharField(max_length=1, choices=room_choice, null=True, blank=True ) #


    


    # def get_price(self):
    #     # all_price= self.price=(self.numberOfDays * self.numberOfRooms)
        
    #     if self.room_type == 'S':
    #         return self.numberOfDays * self.numberOfRooms
    #     elif self.room_type == 'D':
    #         return self.numberOfDays * self.numberOfRooms * 2
    #     else:
    #         return 0

    def __str__(self):
        return f'{self.user.username} - {self.user.email}'

