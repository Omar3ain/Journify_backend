from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from stripe.error import AuthenticationError
from django.conf import settings
from hotelReservation.models import StayReservation
from flight.models import Flight_Reservation
from .models import Payment
import stripe
from django.views.decorators.csrf import csrf_exempt
import secrets
import json
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

stripe.api_key = 'sk_test_51NPUYhA5woj6pmWHKnBPkOJJWYMt6mA9Kj66uLdeAxdrZEXoy1dOBZe0zGErSHwyGxfEsG1uyZH8fICTIt6KqXah007YjZmOkx'

@csrf_exempt
def HotelCheckout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data['amount']
            
            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card']
            )
            
            # Return the client secret
            return JsonResponse({'paymentIntent': payment_intent.client_secret})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# class HotelCheckout(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         user = request.user
#         hotelDetails = Payment.get_stay_by_id(self, pk)
#         if type(hotelDetails) is Response:
#             return hotelDetails

#         # make checkout session
#         line_items = [{
#             'price_data': {
#                 'currency': 'usd',
#                 'unit_amount': int(hotelDetails.price * 100),
#                 'product_data': {
#                     'name': hotelDetails.hotel.name,
#                     'description': f"Number of rooms: {hotelDetails.numberOfRooms}   --   Number of people: {hotelDetails.numberOfPeople}  --  Number of days: {hotelDetails.numberOfDays}  --  Room type: {hotelDetails.room_type}",
#                 },
#             },
#             'quantity': 1,
#         }]

#         try:
#             token = secrets.token_hex(16)  # generate a random payment token
#             base_url = request.scheme + '://' + request.get_host()
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=f'{base_url}/payment/hotel-success?token={token}&user={user.id}&hotelDetails={hotelDetails.id}',
#                 cancel_url=f'{base_url}/payment/hotel-checkout/',
#             )

#         except AuthenticationError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'url': checkout_session.url})


class FlightCheckout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        flightDetails = Payment.get_flight_by_id(self, pk)
        if type(flightDetails) is Response:
            return flightDetails

        # make checkout session
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(flightDetails.flight.ticket_price * 100),
                'product_data': {
                    "name": f"{flightDetails.flight.company_name} - {flightDetails.flight.origin} to {flightDetails.flight.destination}",
                    'description': f"Date: {flightDetails.flight.traveling_date} - {flightDetails.number_seats} Seats",
                },
            },
            'quantity': 1,
        }]

        try:
            token = secrets.token_hex(16)  # generate a random payment token
            base_url = request.scheme + '://' + request.get_host()
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=f'{base_url}/payment/flight-success?token={token}&user={user.id}&flightDetails={flightDetails.id}',
                cancel_url=f'{base_url}/payment/flight-checkout/',
            )

        except AuthenticationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'url': checkout_session.url})


class FlightPaymentSuccess(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.GET.get('token')
        user = request.GET.get('user')
        flightDetails = request.GET.get('flightDetails')

        if token is None or user is None or flightDetails is None:
            return Response({'error': 'token, user and stay parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        pToken = Payment.objects.create(
            payment_id=token,
            flightResId=Flight_Reservation.objects.get(pk=flightDetails),
            status=True
        )
        pToken.save()
        return Response({'message': 'Payment completed successfully'}, status=status.HTTP_200_OK)


class HotelPaymentSuccess(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.GET.get('token')
        user = request.GET.get('user')
        hotelDetails = request.GET.get('hotelDetails')

        if token is None or user is None or hotelDetails is None:
            return Response({'error': 'token, user and stay parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        pToken = Payment.objects.create(
            payment_id=token,
            stayResId=StayReservation.objects.get(pk=hotelDetails),
            status=True
        )
        pToken.save()
        return Response({'message': 'Payment completed successfully'}, status=status.HTTP_200_OK)
