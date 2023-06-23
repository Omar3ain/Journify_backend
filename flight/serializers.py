import re
import pytz
import datetime
from .models import Flight
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class FlightSerializer(serializers.ModelSerializer, CountryFieldMixin):
    origin = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = '__all__'
        read_only_fields = ['companyName', 'travelingDate', 'ticketPrice','availableSeats']

    def get_origin(self, obj):
        return obj.origin.name if obj.origin else None

    def get_destination(self, obj):
        return obj.destination.name if obj.destination else None
    
    def validate_traveling_date(self, value):
        if value < datetime.datetime.now(tz=pytz.utc):
            raise serializers.ValidationError('Traveling date cannot be in the past.')
        return value

    def create(self, validated_data):
        flight = Flight(**validated_data)
        flight.save()
        return flight
    
    
    def update(self, instance, validated_data):
        
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.traveling_date = validated_data.get('traveling_date', instance.traveling_date)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.ticket_price = validated_data.get('ticket_price', instance.ticket_price)
        instance.available_seats = validated_data.get('available_seats', instance.available_seats)
        instance.save()
        return instance
