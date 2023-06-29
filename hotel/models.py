from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from country.models import Country
from django.apps import apps

class Hotel(models.Model):
    name = models.CharField(
        'hotelName', blank=False, max_length=15, null=False, validators=[MinLengthValidator(3)])
    description = models.CharField(
        'hotelDescription', blank=False, max_length=150, null=False, validators=[MinLengthValidator(3)])
    countryId = models.ForeignKey(Country, on_delete=models.CASCADE)
    image = models.CharField('hotelImage', blank=False, max_length=150, null=False, validators=[MinLengthValidator(3)])
    room_price = models.PositiveIntegerField('roomPrice', blank=False, null=False, validators=[
                                                MinValueValidator(15), MaxValueValidator(7000)])
    available_rooms = models.IntegerField(
        'availableRooms', blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(70)])
    longitude = models.CharField('longitude', blank=False, max_length=15, null=False, validators=[MinLengthValidator(3)])
    latitude = models.CharField('latitude', blank=False, max_length=15, null=False, validators=[MinLengthValidator(3)])
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name}:{self.description}'

    def update_avg_rating(self):
        HotelReview = apps.get_model('hotelReview', 'HotelReview')
        reviews = HotelReview.objects.filter(hotel_id=self.id)
        total_reviews = len(reviews)
        if total_reviews > 0:
            total_rating = sum(review.rating for review in reviews)
            self.avg_rating = total_rating / total_reviews
        else:
            self.avg_rating = 0
        self.save()
