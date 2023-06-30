from django.urls import path

from .views import PlaceInfo

urlpatterns = [
    path('<str:xid>/', PlaceInfo.as_view(), name='PlaceInfo'),
]
