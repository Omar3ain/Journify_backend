import requests
from django.http import JsonResponse
from hotelReservation.models import StayReservation
from country.models import Country
import os

from dotenv import load_dotenv
load_dotenv()

def get_trip_plans(request):
    url = 'https://ai-trip-planner.p.rapidapi.com/'
    userId = request.headers.get('userId')
    stays = StayReservation.objects.filter(user_id=userId)

    if not stays:
        return JsonResponse({'error': 'No stay reservations found for the user.'})
    
    last_stay = stays.last()
    # country = Country.objects.get(id=)
    params = {
        'days': '3',
        'destination':  last_stay.hotel.city + ',' + last_stay.hotel.countryId.code
    }
    headers = {
        'X-RapidAPI-Key': '0690936387msha83dcad864a8b9ep1153b8jsncc728f419c2b',
        'X-RapidAPI-Host': 'ai-trip-planner.p.rapidapi.com'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        return JsonResponse(data)  # Return the trip plans as a JSON response
    except requests.exceptions.RequestException as error:
        return JsonResponse({'error': str(error)})
