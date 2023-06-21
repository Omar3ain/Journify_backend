from rest_framework import serializers
from .models import User
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def get_age(self, obj):
        if obj.dob:
            today = date.today()
            age = today.year - obj.dob.year - ((today.month, today.day) < (obj.dob.month, obj.dob.day))
            return age
        else:
            return None

    def validate_dob(self, dob):
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise serializers.ValidationError("You must be 18 years or older to register.")
        return dob

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)    
        instance.image = validated_data.get('image', instance.image)
        instance.dob = validated_data.get('dob', instance.dob)
        # self.validate_dob(dob)
        # instance.dob = dob
        instance.save()
        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        dob = validated_data.get('dob')
        self.validate_dob(dob)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user