"""
URL configuration for journify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('city/', include('city.urls')),
    path('country/', include('country.urls')),
    path('flight/', include('flight.urls')),
    path('hotel/', include('hotel.urls')),
    path('stayreservation/', include('hotelReservation.urls')),
    path('payment/', include('payment.urls')),
    path('properties/', include('properties.urls')),
    path('recommendation/', include('recommendation.urls')),
    path('jplans/', include('journey_plans.urls')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
]
