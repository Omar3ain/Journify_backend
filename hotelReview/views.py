from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import HotelReview
from .serializers import HotelReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

class HotelReviewCreateView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = HotelReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except IntegrityError as e:
            error_message = "The fields user and hotel must make a unique set."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class UpdateReviewView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelReviewSerializer
    queryset = HotelReview.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class DeleteReviewView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelReviewSerializer
    queryset = HotelReview.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            return Response({"error": "You are not authorized to delete this review"}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()