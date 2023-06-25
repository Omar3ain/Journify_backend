from django.urls import path
from .views import (
    HotelListView
    
)

app_name = 'reservations'
urlpatterns = [
    path('', HotelListView.as_view(), name='list'),
]