from django.urls import path
from .views import HotelCheckout, FlightCheckout, HotelPaymentSuccess, FlightPaymentSuccess

urlpatterns = [
    path('hotel-checkout/<str:pk>/', HotelCheckout.as_view()),
    path('flight-checkout/<str:pk>/', FlightCheckout.as_view()),
    path('hotel-success/', HotelPaymentSuccess.as_view()),
    path('flight-success/', FlightPaymentSuccess.as_view()),
]
