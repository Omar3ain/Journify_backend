from django.urls import path
from .views import CountryAPIView, GeoLocationAPI

urlpatterns = [
    path('', CountryAPIView.as_view(), name='list_country'),
    path('geolocation/', GeoLocationAPI.as_view(), name='get_cities')
]