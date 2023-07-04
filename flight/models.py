import pytz
import datetime
from django.utils import timezone
from django.db import models
from user.models import User
from django.db.models.functions import Now
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

# Create your models here.

class Flight_ReservationManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        # return super().get_queryset(*args, **kwargs).filter(
        #     expiration_time__lt=timezone.now()
        # )
        return super().get_queryset(*args, **kwargs)


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

    flight = models.ForeignKey(
        Flight, related_name="flight", on_delete=models.CASCADE)

    number_seats = models.PositiveIntegerField(
        'seatsNumber', validators=[MinValueValidator(1), MaxValueValidator(15)])

    flightClass = models.CharField(max_length=8, choices=[
        ('Economy', 'Economy'),
        ('Business', 'Business')], default="Economy")

    status = models.CharField(max_length=100, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)

    expiration_time = models.DateTimeField(
        db_index=True, default=timezone.now() + timezone.timedelta(days=2), editable=False)
    objects = Flight_ReservationManager()

    def __str__(self):
        return f'{self.flight.origin.name}:{self.flight.destination.name}--{self.user_id}-- at {self.flight.traveling_date}'

    def confirm(self, payment_intent_id):
        self.status = 'confirmed'
        self.payment_intent_id = payment_intent_id
        self.save()

    def cancel(self):
        self.status = 'cancelled'
        self.save()