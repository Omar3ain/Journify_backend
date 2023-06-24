import asyncio
import aiohttp
from django.http import JsonResponse

async def fetch_details(session, xid, headers):
    url = f'https://opentripmap-places-v1.p.rapidapi.com/en/places/xid/{xid}'
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def get_data_async(params):
    url = 'https://opentripmap-places-v1.p.rapidapi.com/en/places/radius'
    headers = {
        'X-RapidAPI-Key': '4532d6561cmsh43c9fefc912e7aap1934b0jsn4dbb3e87b432',
        'X-RapidAPI-Host': 'opentripmap-places-v1.p.rapidapi.com'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            data = await response.json()
            xids = []
            if 'features' in data:
                xids = [feature['properties']['xid'] for feature in data['features']]

            tasks = []
            for xid in xids:
                task = asyncio.ensure_future(fetch_details(session, xid, headers))
                tasks.append(task)

            details_data = await asyncio.gather(*tasks)
            return details_data

def get_data(request):
    radius = request.GET.get('radius', '500')
    name = request.GET.get('name')
    kinds = request.GET.get('kinds')

    params = {
        'lat': '59.855685', #
        'lon': '38.364285', #
        'radius': radius or '500',
        'limit': '25',
    }

    if name:
        params['name'] = name
    if kinds:
        params['kinds'] = kinds

    details_data = asyncio.run(get_data_async(params))
    return JsonResponse(details_data, safe=False)
