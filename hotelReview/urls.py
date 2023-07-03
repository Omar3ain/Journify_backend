from django.urls import path
from .views import HotelReviewCreateView, UpdateReviewView, DeleteReviewView, HotelReviewGetView

urlpatterns = [
    path('<int:hotel_id>/', HotelReviewGetView.as_view(), name="hotel-review-get"),
    path("create/", HotelReviewCreateView.as_view(), name="hotel-review-create"),
    path('update/<int:pk>/', UpdateReviewView.as_view(), name='hotel-review-update'),
    path('delete/<int:pk>/', DeleteReviewView.as_view(), name='hotel-review-delete'),
]