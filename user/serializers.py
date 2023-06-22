from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
import re

# Custom password validators
class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'\d', password):
            raise ValidationError(
                "The password must contain at least 1 digit, 0-9.",
                code='password_no_number',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 digit, 0-9."


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                "The password must contain at least 1 uppercase letter, A-Z.",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 uppercase letter, A-Z."


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                "The password must contain at least 1 special character: " +
                "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?",
                code='password_no_symbol',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 special character: " \
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"


class RepeatedValidator(object):
    def validate(self, password, user=None):
        # In case there is no user, this validator is not applicable, so we return success
        if user is None:
            return None

        # Your logic for checking repeated passwords goes here
        # ...

    def password_changed(self, password, user=None):
        # In case there is no user, this is not applicable
        if user is None:
            return None

        # Your logic for saving the changed password goes here
        # ...

    def get_help_text(self):
        return "Your password cannot be the same as previously used passwords."


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['username', 'email', 'dob']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        # Validate the password using Django's built-in validators
        validate_password(value, user=self.instance)

        # Add custom password validation rules using the custom validators
        validators = [
            NumberValidator(),
            UppercaseValidator(),
            SymbolValidator(),
            RepeatedValidator(),
        ]

        for validator in validators:
            validator.validate(value, user=self.instance)

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        dob = validated_data.get('dob')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
