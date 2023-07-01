from django.urls import path
from .views import (
    HotelListView,
    HotelDetails
    
)

app_name = 'hotels'
urlpatterns = [
    path('', HotelListView.as_view(), name='list'),
    path('<int:hotel_id>', HotelDetails.as_view(), name='hotel_details')
]