from django.db import models
from flight.models import Flight_Reservation
from hotelReservation.models import StayReservation
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


class Payment(models.Model):
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    flightResId = models.ForeignKey(
        Flight_Reservation, on_delete=models.CASCADE, null=True, blank=True)
    stayResId = models.ForeignKey(
        StayReservation, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    
    def get_stay_by_id(self, pk):
        try:
            return StayReservation.objects.get(pk=pk)
        except StayReservation.DoesNotExist:
            return Response({'error': 'No hotel reservation found'}, status=status.HTTP_404_NOT_FOUND)
        

    # one of the two foriegn keys should be null and the other should be not null
    def clean(self):
        if self.flightResId is None and self.stayResId is None:
            raise ValidationError(
                'Both flightResId and stayResId cannot be null')
        if self.flightResId is not None and self.stayResId is not None:
            raise ValidationError(
                'Both flightResId and stayResId cannot be not null')

    # override model's save method to make it always call the clean() method before triggering the Model class save method
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        # get the user's email from the flight reservation or the hotel reservation
        return f'{self.flightResId.user.email if self.flightResId is not None else self.stayResId.user.email} - {self.payment_id}'
