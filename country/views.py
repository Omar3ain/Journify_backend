from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Country
from .serializers import CountrySerializer
from django_countries.fields import CountryField
from geopy.geocoders import Nominatim
from django.http import JsonResponse


class CountryAPIView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def put(self, request, pk):
        country = self.get_object(pk)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        country = self.get_object(pk)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# get coordinates of a city or country using django-countries and geopy
class GeoLocationAPI(APIView):
    def get(self, request):
        country_name = request.GET.get('name')

        # Retrieve the country object using the django-countries package
        country = CountryField(name=country_name)

        # Use a geocoder (e.g., Nominatim) to fetch city coordinates
        geolocator = Nominatim(user_agent="journify")
        location = geolocator.geocode(country.name)

        # Check if location exists and retrieve the latitude and longitude
        geolocation = []
        if location:
            latitude = location.latitude
            longitude = location.longitude

            geolocation.append({
                'name': location.address,
                'latitude': latitude,
                'longitude': longitude
            })

        return Response({'geolocation': geolocation})
