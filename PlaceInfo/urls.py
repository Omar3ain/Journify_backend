from django.urls import path

from .views import PlaceInfo, get_popular_places

urlpatterns = [
    path('popular/', get_popular_places, name='most-popular-places'),
    path('search/', get_popular_places, name='search-places'),
    path('<str:xid>/', PlaceInfo.as_view(), name='PlaceInfo'),
]
