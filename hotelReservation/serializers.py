from rest_framework import serializers
from .models import StayReservation
from user.models import User
from datetime import datetime
import pytz




class StayReservationSerializer(serializers.ModelSerializer):
    user=User()
    class Meta:
        model = StayReservation
        exclude=['user','price']


    def validate_reserving_date(self, value):
        if value < datetime.datetime.now(tz=pytz.utc):
            raise serializers.ValidationError(
                'Reservation date cannot be in the past.')
        return value














# class StayReservationViewSet(viewsets.ModelViewSet):
#     queryset = StayReservation.objects.all()
#     serializer_class = StayReservationSerializer

#     @action(methods=['post'], detail=False)
#     def calculate_price(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         price = serializer.validated_data['numberOfDays'] * serializer.validated_data['numberOfRooms']
#         return Response({'price': price}, status=status.HTTP_200_OK)