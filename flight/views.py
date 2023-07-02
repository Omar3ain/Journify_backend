import pytz
import datetime
from django.utils import timezone
from rest_framework import generics
from django.shortcuts import get_object_or_404, render
from .serializers import FlightSerializer, EditReservationsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Flight, Flight_Reservation
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.core.exceptions import ValidationError


class ListFlightsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FlightSerializer

    def get_queryset(self):
        requested_origin = self.request.query_params['from']
        requested_destination = self.request.query_params['to']
        print("flight", Flight.objects.filter(origin__exact=requested_origin))
        return Flight.objects.filter(origin__exact=requested_origin, destination__exact=requested_destination, traveling_date__gt=datetime.datetime.now(tz=pytz.utc))


class GetFlightView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            flight = Flight.objects.get(id=pk)
            print(flight)
        except Flight.DoesNotExist:
            return Response({'detail': 'Flight not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FlightSerializer(flight)
        return Response(serializer.data)


class FlightView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightSerializer

    def get_queryset(self):
        return Flight.objects.filter(traveling_date__gt=datetime.datetime.now(tz=pytz.utc))

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(
                instance, data=request.data, context={"flight_id": pk}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Flight.DoesNotExist:
            return Response({"error": "Flight doesn't exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def destroy(self, request, pk, action=None, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=pk)
            instance.delete()
            return Response({'detail': 'Flight deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Flight.DoesNotExist:
            return Response({'detail': 'Flight not found.'}, status=status.HTTP_404_NOT_FOUND)


class ListFlight_ReservationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditReservationsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Flight_Reservation.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


class FlightReservationView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditReservationsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Flight_Reservation.objects.filter(user_id=user_id)

    def post(self, request, pk, *args, **kwargs):
        data = {"user_id": request.user.id, "flight": pk,
                "number_seats": request.data["number_seats"], "flightClass":request.data["flightClass"]}
        serializer = self.get_serializer(
            data=data, context={"user": request.user, "flight_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, action, *args, **kwargs):
        try:
            instance = self.get_queryset().filter(flight=pk).first()
            serializer = self.get_serializer(
                instance, data=request.data, context={"action": action, "flight_id": pk, "user": request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Flight_Reservation.DoesNotExist:
            return Response({"error": "Reservation doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk, action=None, *args, **kwargs):
        try:
            instance = self.get_queryset().get(flight=pk)
            flight = Flight.objects.get(id=pk)
            if ((flight.traveling_date - timezone.now()) <= datetime.timedelta(days=2)):
                return Response({"error": "Reservations can only be cancelled before 2 days"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                flight.available_seats += instance.number_seats
                flight.save()
                instance.delete()
                return Response(status=status.HTTP_200_OK)
        except Flight_Reservation.DoesNotExist:
            return Response({"error": "Reservation doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
