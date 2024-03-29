from rest_framework import serializers
from .models import HotelReview

class HotelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReview
        fields = '__all__'
        
    def create(self, validated_data):
      validated_data['user'] = self.context['request'].user
      return super().create(validated_data)