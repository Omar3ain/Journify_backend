import re
import pytz
import datetime
import stripe
from django.forms.models import model_to_dict
from .models import Flight, Flight_Reservation
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


def edit_flight_availableSeats(flight: Flight, seats: int):
    if (flight.available_seats - seats < 0):
        if (flight.available_seats == 0):
            raise serializers.ValidationError(
                {'error': ['Flight is full']}, 422)
        else:
            raise serializers.ValidationError(
                {'error': [f' Only {flight.available_seats} seats available.']}, 422)
    else:
        flight.available_seats -= seats
        flight.save()


class FlightSerializer(serializers.ModelSerializer, CountryFieldMixin):
    origin = serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = '__all__'
        read_only_fields = ['companyName', 'travelingDate',
                            'ticketPrice', 'availableSeats']

    def get_origin(self, obj):
        return obj.origin.name if obj.origin else None

    def get_destination(self, obj):
        return obj.destination.name if obj.destination else None

    def validate_traveling_date(self, value):
        if value < datetime.datetime.now(tz=pytz.utc):
            raise serializers.ValidationError(
                'Traveling date cannot be in the past.')
        return value

    def create(self, validated_data):
        flight = Flight(**validated_data)
        flight.save()
        return flight

    def update(self, instance, validated_data):

        instance.company_name = validated_data.get(
            'company_name', instance.company_name)
        instance.traveling_date = validated_data.get(
            'traveling_date', instance.traveling_date)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get(
            'destination', instance.destination)
        instance.ticket_price = validated_data.get(
            'ticket_price', instance.ticket_price)
        instance.available_seats = validated_data.get(
            'available_seats', instance.available_seats)
        instance.save()
        return instance


class EditReservationsSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Flight_Reservation
        fields = ["id", "number_seats", "flight",
                  "total_price", "flightClass", "status", "expiration_time"]

    def get_total_price(self, obj):
        return obj.flight.ticket_price * obj.number_seats * (2 if obj.flightClass == "Business" else 1)

    def create(self, validated_data):
        user = self.context['user']
        flight_id = self.context['flight_id']
        reservation_exist = Flight_Reservation.objects.filter(
            user_id=user, flight=flight_id).first()
        if (reservation_exist):
            raise serializers.ValidationError(
                {'error': ['Reservation already exist.']}, 400)
        else:
            try:
                flight = Flight.objects.get(id=flight_id)

                reserved_flight = Flight_Reservation.objects.create(
                    user_id=user, flight=flight, number_seats=validated_data['number_seats'], flightClass=validated_data['flightClass'])

                edit_flight_availableSeats(
                    flight, validated_data['number_seats'])

                reserved_flight.save()
                return reserved_flight

            except Flight.DoesNotExist:
                raise serializers.ValidationError(
                    {'error': ['flight does not exist.']}, 404)

    def update(self, instance, validated_data):
        flight_id = self.context.get('flight_id', None)
        status = validated_data.get('status', None)
        payment_intent_id = validated_data.get('paymentId', None)

        try:
            flight = Flight.objects.get(id=flight_id)
            if (status):
                instance.status = status
                if (status == "cancelled"):
                    flight.available_seats += instance.number_seats
                    instance.delete()
                    return instance

                if (status == "pending"):
                    raise serializers.ValidationError(
                        {'error': ['Invalid reservation']}, 400)

            if (payment_intent_id):
                instance.payment_intent_id = payment_intent_id

            instance.save()
            return instance

        except Flight.DoesNotExist:
            raise serializers.ValidationError(
                {'error': "Flight doesn't exist"}, code=422)