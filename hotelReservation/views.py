# from django.views.generic import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from .models import StayReservation
from rest_framework.response import Response
# from rest_framework.exceptions import NotFound
from rest_framework import status, generics
# from rest_framework import serializers
from .serializers import StayReservationSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from hotel.models import Hotel
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import stripe


def get_payment_secret(price, user):
    stripe.api_key = "sk_test_51NPVMMG8QYLQRO7Qd5iNUQuGPEVP2FizkQsgkCHgPpkkwh0TMe3UuvUnOFesiUaICB4HNQCKXj8lC7b94cGfliL300zU4d10fH"
    intent = stripe.PaymentIntent.create(
        amount=price,
        currency="egp",
        metadata={'userid': user.id})
    return intent


class ReservationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = StayReservation.objects.all()
    serializer_class = StayReservationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return StayReservation.objects.filter(user=user)
        else:
            return StayReservation.objects.none()


class CreateReservation(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StayReservationSerializer

    def get_queryset(self):
        return StayReservation.objects.all()

    def post(self, request):
        if not self.request.user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            number_of_days = request.data.get('numberOfDays')
            number_of_rooms = request.data.get('numberOfRooms')
            number_of_people = request.data.get('numberOfPeople')
            room_type = request.data.get('room_type')
            hotel_id = request.data.get('hotel')
            start_date = request.data.get('startDate')
            hotel = Hotel.objects.get(id=hotel_id)

            hotel.available_rooms -= int(number_of_rooms)
            if hotel.available_rooms < 1:
                return Response({'error': 'No available rooms'}, status=status.HTTP_400_BAD_REQUEST)
            hotel.save()

            if not number_of_days or not number_of_rooms or not room_type:
                return Response({'error': 'numberOfDays, numberOfRooms, StartDate and room_type are required'}, status=status.HTTP_400_BAD_REQUEST)

            # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            all_price = self.get_price(
                room_type, number_of_days, number_of_rooms, hotel.room_price)
            user = self.request.user  # Get the authenticated user
            reservation = StayReservation(
                user=user,
                room_type=room_type,
                hotel=hotel,
                numberOfRooms=number_of_rooms,
                price=all_price,
                numberOfDays=number_of_days,
                numberOfPeople=number_of_people,
                startDate=start_date
            )
            reservation.save()
            serializer = StayReservationSerializer(reservation)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({**serializer.data, "client_secret": get_payment_secret(all_price, user)}, status=status.HTTP_201_CREATED)

        except Hotel.DoesNotExist:
            return Response({"error": "Hotel doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def get_price(self, room_type, number_of_days, number_of_rooms, room_price):
        if room_type == 'S':
            return int(number_of_days) * int(number_of_rooms) * int(room_price)
        elif room_type == 'D':
            return int(number_of_days) * int(number_of_rooms) * int(room_price) * 2
        else:
            return 0  # Return a default price or handle the invalid room_type case as needed


class EditReservation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StayReservationSerializer

    def get_queryset(self):
        return StayReservation.objects.all()

    def patch(self, request, pk, *args, **kwargs):
        instance = self.get_queryset().filter(hotel=hotel).first()
        if instance:
                serializer = self.get_serializer(
                    instance, data=request.data, context={"hotel_id": pk, "user": request.user}, partial=True)
        else:
                return Response({"error": "Reservation doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



# class StayReservationListView(ListView):
#     model = StayReservation
#     template_name = 'reservations/list.html'
#     context_object_name = 'reservations'

# class StayReservationCreateView(CreateView):
#     model = StayReservation
#     fields = ['userId', 'hotelId', ' numberOfRooms', 'numberOfPeople', 'startDate', 'numberOfDays', 'price']
#     template_name = 'reservations/create.html'
#     success_url = reverse_lazy('reservations:list')

# class StayReservationDetailView(DetailView):
#     model = StayReservation
#     template_name = 'reservations/detail.html'
#     context_object_name = 'reservation'

# class StayReservationUpdateView(UpdateView):
#     model = StayReservation
#     fields = ['userId', 'hotelId', 'numberOfRooms', 'numberOfPeople', 'startDate', 'numberOfDays', 'price']
#     template_name = 'reservations/update.html'
#     success_url = reverse_lazy('reservations:list')

# class StayReservationDeleteView(DeleteView):
#     model = StayReservation
#     template_name = 'reservations/delete.html'
#     success_url = reverse_lazy('reservations:list')
