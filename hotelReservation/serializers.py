from rest_framework import serializers
from .models import StayReservation
from user.models import User



class StayReservationSerializer(serializers.ModelSerializer):
    user=User()
    class Meta:
        model = StayReservation
        exclude=['user','price']














# class StayReservationViewSet(viewsets.ModelViewSet):
#     queryset = StayReservation.objects.all()
#     serializer_class = StayReservationSerializer

#     @action(methods=['post'], detail=False)
#     def calculate_price(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         price = serializer.validated_data['numberOfDays'] * serializer.validated_data['numberOfRooms']
#         return Response({'price': price}, status=status.HTTP_200_OK)