import pytz
import datetime
from django.db import models
from  user.models import  User
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

# Create your models here.

class Flight(models.Model):
    company_name = models.CharField(
        'companyName', blank=False, max_length=15, null=False, validators=[MinLengthValidator(3)])
    traveling_date = models.DateTimeField('travelingDate', blank=False, null=False, validators=[
                                          MinValueValidator(datetime.datetime.now(tz=pytz.utc))])
    origin = CountryField(null=False, blank=False)
    destination = CountryField(null=False, blank=False)
    ticket_price = models.PositiveIntegerField('ticketPrice', blank=False, null=False, validators=[
                                               MinValueValidator(1000), MaxValueValidator(10000)])
    available_seats = models.IntegerField(
        'availableSeats', blank=False, null=False, validators=[MinValueValidator(1), MaxValueValidator(400)])

    def __str__(self):
        return f'{self.origin.name}:{self.destination.name}'


class Flight_Reservation(models.Model):
    user_id = models.ForeignKey(
        User, related_name="user", on_delete=models.DO_NOTHING)
    flight_id = models.ForeignKey(
        Flight, related_name="flight", on_delete=models.CASCADE)
    number_seats = models.PositiveIntegerField(
        'seatsNumber', validators=[MinValueValidator(1), MaxValueValidator(15)])

    def __str__(self):
        return f'{self.flight_id.origin.name}:{self.flight_id.destination.name}--{self.user_id}-- at {self.flight_id.traveling_date}'
