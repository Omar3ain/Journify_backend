import requests
from django.http import JsonResponse

def get_trip_plans(request):
    url = 'https://ai-trip-planner.p.rapidapi.com/'
    params = {
        'days': '3',
        'destination': 'London,UK'
    }
    headers = {
        'X-RapidAPI-Key': '4532d6561cmsh43c9fefc912e7aap1934b0jsn4dbb3e87b432',
        'X-RapidAPI-Host': 'ai-trip-planner.p.rapidapi.com'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        return JsonResponse(data)  # Return the trip plans as a JSON response
    except requests.exceptions.RequestException as error:
        return JsonResponse({'error': str(error)})
