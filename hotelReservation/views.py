# from django.views.generic import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from .models import StayReservation
from rest_framework.response import Response
# from rest_framework.exceptions import NotFound
from rest_framework import status, generics
# from rest_framework import serializers
from .serializers import  StayReservationSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from hotel.models import Hotel
from rest_framework.response import Response
from rest_framework import status




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
            return Response({'error':'user Is not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
        number_of_days = request.data.get('numberOfDays')
        number_of_rooms = request.data.get('numberOfRooms')
        number_of_people = request.data.get('numberOfPeople')
        hotel_id = request.data.get('hotel')
        hotel = Hotel.objects.get(id=hotel_id)
        if hotel.available_rooms < 1:
            return Response({'error': 'no available rooms'}, status=status.HTTP_400_BAD_REQUEST)

        hotel.available_rooms-=1
        hotel.save()

        if not number_of_days or not number_of_rooms:
            return Response({'error': 'numberOfDays and numberOfRooms are required'}, status=status.HTTP_400_BAD_REQUEST)

        all_price = int(number_of_days) * int(number_of_rooms)
        user = self.request.user  # Get the authenticated user
        reservation = StayReservation(user=user, hotel=hotel, numberOfRooms=number_of_rooms, price=all_price, numberOfDays=number_of_days, numberOfPeople=number_of_people)
        reservation.save()
        serializer = StayReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    # def put(self, request, pk):
    #     try:
    #         reservation = StayReservation.objects.get(pk=pk)
    #     except StayReservation.DoesNotExist:
    #         return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = self.serializer_class(reservation, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     try:
    #         reservation = StayReservation.objects.get(pk=pk)
    #     except StayReservation.DoesNotExist:
    #         return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)
        
    #     reservation.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
        
    

    




































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