from django.urls import path
from . import views

app_name = 'journey_plans'

urlpatterns = [
    path('', views.get_trip_plans, name='journey_plans'),
]
