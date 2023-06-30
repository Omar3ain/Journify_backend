from django.urls import path
from .views import HotelCheckout, PaymentSuccess

urlpatterns = [
    path('hotel-checkout/<str:pk>/', HotelCheckout.as_view()),
    path('success/', PaymentSuccess.as_view()),
]
