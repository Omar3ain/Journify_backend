from django.db import models
from user.models import User

# Create your models here.
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # flightResId = models.ForeignKey('flight.FlightReservation', on_delete=models.CASCADE) # flightResId
    # staysResId = models.ForeignKey('stays.StaysReservation', on_delete=models.CASCADE) # staysResId
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.payment_id)
