import asyncio
import aiohttp
from django.http import JsonResponse
from hotelReservation.models import StayReservation
from django.shortcuts import get_object_or_404
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
    radius = request.GET.get('radius', '5000')
    name = request.GET.get('name')
    kinds = request.GET.get('kinds')
    userId = request.headers.get('userId')
    # stays = StayReservation.objects.filter(user_id=userId)
    
    # if not stays:
    #     return JsonResponse({'error': 'No stay reservations found for the user.'})
    
    # last_stay = stays.last()
    
    params = {
        'lat': '48.8534951',
        'lon': '2.3483915',
        'radius': radius or '5000',
        'limit': '35',
        'kinds': kinds or 'cultural,historic',
    }
    
    if name:
        params['name'] = name
    
    details_data = asyncio.run(get_data_async(params))
    return JsonResponse(details_data, safe=False)