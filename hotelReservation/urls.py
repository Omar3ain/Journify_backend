from django.urls import path
from .views import (
    ReservationList,
    CreateReservation,
    
)

app_name = 'hotels'
urlpatterns = [
    path('', ReservationList.as_view(), name='list'),
    path('create/', CreateReservation.as_view(), name='create'),
    # path('<int:pk>/', StayReservationDetailView.as_view(), name='detail'),
    # path('<int:pk>/update/', StayReservationUpdateView.as_view(), name='update'),
    # path('<int:pk>/delete/', StayReservationDeleteView.as_view(), name='delete'),
]