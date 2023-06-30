from django.http import JsonResponse
from django.views import View
import requests

class PlaceInfo(View):
    def get(self, request, xid):
        url = f'https://opentripmap-places-v1.p.rapidapi.com/en/places/xid/{xid}'
        headers = {
            'X-RapidAPI-Key': '4532d6561cmsh43c9fefc912e7aap1934b0jsn4dbb3e87b432',
            'X-RapidAPI-Host': 'opentripmap-places-v1.p.rapidapi.com'
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)})
