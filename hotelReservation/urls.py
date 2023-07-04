from django.urls import path
from .views import (
    ReservationList,
    CreateReservation,
    EditReservation,
)

app_name = 'reservations'
urlpatterns = [
    path('', ReservationList.as_view(), name='list'),
    path('create/', CreateReservation.as_view(), name='create'),
    path('edit/<int:pk>', EditReservation.as_view(), name='edit'),
    # path('<int:pk>/', StayReservationDetailView.as_view(), name='detail'),
    # path('<int:pk>/update/', StayReservationUpdateView.as_view(), name='update'),
    # path('<int:pk>/delete/', StayReservationDeleteView.as_view(), name='delete'),
]