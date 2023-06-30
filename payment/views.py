from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from stripe.error import AuthenticationError
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hotelReservation.models import StayReservation
from .models import Payment
import stripe
import secrets

stripe.api_key = settings.STRIPE_SECRET_KEY


class HotelCheckout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        hotelDetails = Payment.get_stay_by_id(self, pk)
        if type(hotelDetails) is Response:
            return hotelDetails

        # make checkout session
        line_items = {
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(hotelDetails.price * 100),
                'product_data': {
                    'name': hotelDetails.hotel.name,
                    'description': f"Number of rooms: {hotelDetails.numberOfRooms} -------- Number of people: {hotelDetails.numberOfPeople} -------- Number of days: {hotelDetails.numberOfDays} -------- Room type: {hotelDetails.room_type}",
                },
            },
            'quantity': 1,
        }

        try:
            token = secrets.token_hex(16)  # generate a random payment token
            base_url = request.scheme + '://' + request.get_host()
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[line_items],
                mode='payment',
                success_url=f'{base_url}/payment/success?token={token}&user={user.id}&hotelDetails={hotelDetails.id}',
                cancel_url=f'{base_url}/payment/hotel-checkout/',
            )

        except AuthenticationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # return redirect(checkout_session.url , code=303)
        return Response({'url': checkout_session.url})


class PaymentSuccess(APIView):
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
