from django.urls import path
from .views import CountryAPIView, CountryDetailAPIView, GeoLocationAPI

urlpatterns = [
    path('', CountryAPIView.as_view(), name='list_country'),
    path('<int:pk>/', CountryDetailAPIView.as_view(), name='detail_country'),
    path('geolocation/', GeoLocationAPI.as_view(), name='get_geolocation'),
]