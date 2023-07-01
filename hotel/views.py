from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel
from .serializers import HotelSerializer
from django.shortcuts import render, get_object_or_404




class HotelListView(APIView):
    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class HotelDetails(APIView):
    def get(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_200_OK)
