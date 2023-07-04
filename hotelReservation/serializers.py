from rest_framework import serializers
from hotel.models import Hotel
from .models import StayReservation
from user.models import User
from datetime import datetime
import pytz


class StayReservationSerializer(serializers.ModelSerializer):
    user = User()

    class Meta:
        model = StayReservation
        exclude = ['user', 'price']

    def validate_reserving_date(self, value):
        if value < datetime.datetime.now(tz=pytz.utc):
            raise serializers.ValidationError(
                'Reservation date cannot be in the past.')
        return value

    def update(self, instance, validated_data):
        hotel_id = self.context.get('hotel_id', None)
        status = validated_data.get('status', None)
        payment_intent_id = validated_data.get('paymentId', None)

        try:
            hotel = Hotel.objects.get(id=hotel_id)
            if (status):
                instance.status = status
                if (status == "cancelled"):
                    hotel.available_rooms += instance.numberOfRooms
                    instance.delete()
                    return instance

                if (status == "pending"):
                    raise serializers.ValidationError(
                        {'error': ['Invalid reservation']}, 400)

            if (payment_intent_id):
                instance.payment_intent_id = payment_intent_id

            instance.save()
            return instance

        except Hotel.DoesNotExist:
            raise serializers.ValidationError(
                {'error': "Hotel doesn't exist"}, code=404)


# class StayReservationViewSet(viewsets.ModelViewSet):
#     queryset = StayReservation.objects.all()
#     serializer_class = StayReservationSerializer

#     @action(methods=['post'], detail=False)
#     def calculate_price(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         price = serializer.validated_data['numberOfDays'] * serializer.validated_data['numberOfRooms']
#         return Response({'price': price}, status=status.HTTP_200_OK)
