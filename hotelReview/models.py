from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class HotelReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'hotel')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.hotel.update_avg_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.hotel.update_avg_rating()

    def __str__(self):
        return f'Review by {self.user.username} for {self.hotel.name}'
