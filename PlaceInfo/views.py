from django.http import JsonResponse
from django.views import View
import requests
import asyncio
import aiohttp
from django.http import JsonResponse
from recommendation.views import get_data_async
from country.views import get_geolocation
import json


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


def get_popular_places(request):
    city_name = request.GET.get('city_name')
    radius = request.GET.get('radius', '5000')
    name = request.GET.get('name')
    kinds = request.GET.get('kinds')

    geolocation = get_geolocation(request, city_name)
    # get latitude and longitude from geolocation content
    my_json_geo = geolocation.content.decode('utf8').replace("'", '"')
    data = json.loads(my_json_geo)
    lat = data['latitude']
    lon = data['longitude']

    params = {
        'lat': lat or "48.8534951",
        'lon': lon or "2.3483915",
        'radius': radius or '5000',
        'limit': '35',
        'kinds': kinds or 'cultural,historic,interesting_places',
        'rate': '3',
    }

    if name:
        params['name'] = name

    details_data = asyncio.run(get_data_async(params))
    return JsonResponse(details_data, safe=False)
