from django.http import JsonResponse
from django.views import View
import requests
from django.http import JsonResponse
from country.views import get_geolocation
import asyncio
from recommendation.views import get_data_async
import json
import os

from dotenv import load_dotenv
load_dotenv()

class PlaceInfo(View):
    def get(self, request, xid):
        url = f'https://opentripmap-places-v1.p.rapidapi.com/en/places/xid/{xid}'
        headers = {
            'X-RapidAPI-Key': '0690936387msha83dcad864a8b9ep1153b8jsncc728f419c2b',
            'X-RapidAPI-Host': 'opentripmap-places-v1.p.rapidapi.com'
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            return JsonResponse(data)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)})


# same used for search and popular places
def get_popular_places(request):
    city_name = request.GET.get('city_name') or 'Paris'
    radius = request.GET.get('radius', '5000')
    name = request.GET.get('name')
    kinds = request.GET.get('kinds')

    # geolocation = get_geolocation(request, city_name)

    # get latitude and longitude from geolocation content
    # my_json_geo = geolocation.content.decode('utf8').replace("'", '"')
    # data = json.loads(my_json_geo)
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    # make condition on route name
    rate = ''
    if request.path == '/place/popular/':
        rate = '3'

    params = {
        'lat': lat or "48.85341",
        'lon': lon or "2.3488",
        'radius': radius or '5000',
        'limit': '35',
        'kinds': kinds or 'cultural,historic'
    }

    if rate:
        params['rate'] = rate

    if name:
        params['name'] = name

    details_data = asyncio.run(get_data_async(params))
    return JsonResponse(details_data, safe=False)
