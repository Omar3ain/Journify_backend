# from django.views.generic import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from .models import StayReservation
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, generics
from rest_framework import serializers
from .serializers import  StayReservationSerializer



class ReservationList(generics.ListAPIView):
    # queryset = StayReservation.objects.all()
    serializer_class = StayReservationSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return StayReservation.objects.filter(user=user)
        else:
            return StayReservation.objects.none()
        




































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