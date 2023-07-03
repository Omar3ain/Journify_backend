from rest_framework import serializers
from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    countryId=serializers.CharField(source = 'countryId.name')
    class Meta:
        model = Hotel
        fields = '__all__'
