import pytz
import datetime
from rest_framework import generics
from django.shortcuts import get_object_or_404, render
from .serializers import FlightSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Flight
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from journify.permission import IsOwnerOrReadOnly, IsAdminOrUnauthenticatedUser
from rest_framework.response import Response
from django.core.exceptions import ValidationError


class ListFlightsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FlightSerializer
    def get_queryset(self):
        return Flight.objects.filter(traveling_date__gt=datetime.datetime.now(tz=pytz.utc)) 


class GetFlightView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            flight = Flight.objects.get(id= pk)
            print(flight)
        except Flight.DoesNotExist:
            return Response({'detail': 'Flight not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FlightSerializer(flight)
        return Response(serializer.data)
    

class FlightView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = FlightSerializer

    def get_queryset(self):
        return Flight.objects.filter(traveling_date__gt=datetime.datetime.now(tz=pytz.utc))
    
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
