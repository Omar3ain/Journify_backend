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
    stay_id = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user_id = models.ForeignKey(
    #     User, related_name="user", on_delete=models.DO_NOTHING)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=None)
    numberOfRooms=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    numberOfPeople = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    startDate = models.DateField(auto_now_add=True)
    numberOfDays = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=7, decimal_places=2, default=20)

    # def save(self, *args, **kwargs):
        

    #     self.price = (self.numberOfDays * self.numberOfRooms * self.numberOfPeople)

    #     super().save(*args, **kwargs)

    def get_price(self):
        all_price= self.price=(self.numberOfDays * self.numberOfRooms)
        return all_price

    def __str__(self):
        return f'{self.user.username} - {self.user.email}'

