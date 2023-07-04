from django.urls import path
from .views import  ListFlightsView, FlightView, FlightReservationView

urlpatterns = [
    path('', ListFlightsView.as_view(), name='list_flights'),
    path('<int:pk>/', FlightView.as_view(), name='edit_flights'),
    path('<int:pk>/reserve/<str:action>/', FlightReservationView.as_view(), name='flight_reservations'),
]   