from django.urls import path
from recommendation.views import get_data

urlpatterns = [
    path('data/', get_data, name='recommendation-data'),
]
