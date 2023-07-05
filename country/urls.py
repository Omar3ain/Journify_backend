from django.urls import path
from .views import CountryAPIView, CountryDetailAPIView, get_geolocation

urlpatterns = [
    path('', CountryAPIView.as_view(), name='list_country'),
    path('<int:pk>/', CountryDetailAPIView.as_view(), name='detail_country'),
    # path('geolocation/', get_geolocation, name='get_geolocation'),
]
