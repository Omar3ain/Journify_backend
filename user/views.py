from rest_framework import generics
from django.shortcuts import get_object_or_404, render
from .serializers import UserSerializer
from .password_validators import SymbolValidator, LowercaseValidator, UppercaseValidator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from journify.permission import IsOwnerOrReadOnly, IsAdminOrUnauthenticatedUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

for user in User.objects.all():
    Token.objects.get_or_create(user=user)


class ListUsersView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(is_superuser=False)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetUserView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAdminOrUnauthenticatedUser]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        email = self.request.data.get('email')
        username = self.request.data.get('username')
        dob = self.request.data.get('dob')
        # Validate the password
        try:
            validate_password(password)
        except ValidationError as e:
            serializer.fail('password_validation', password_validators=e.error_list)

        # Save the user
        serializer.save(password=password , username=username, email=email, dob=dob,is_active=True )


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, *args, **kwargs):
        try:
            user_id = kwargs['user_id']
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'detail': 'User deleted successfully.'})
    
class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['user_id'])

    def get_object(self):
        return self.get_queryset().first()

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                loggedUser = get_object_or_404(User, username=username)
                serializer = UserSerializer(loggedUser)
                token, created = Token.objects.get_or_create(user=user)
            except Token.DoesNotExist:
                print('Token does not exist')
            return Response({'token': token.key , 'user': serializer.data })
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)
        
        
class UserChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if current_password == new_password:
            return Response({'detail': 'New password must be different from current password.'}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(current_password, user.password):
            return Response({'detail': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'detail': 'New password and confirm password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'detail': 'New password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

        lowercase_validator = LowercaseValidator()
        try:
            lowercase_validator.validate(new_password)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        uppercase_validator = UppercaseValidator()
        try:
            uppercase_validator.validate(new_password)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        symbol_validator = SymbolValidator()
        try:
            symbol_validator.validate(new_password)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'dob': user.dob,
            'phone': user.phone,
            'image': user.image.url if user.image else None,
            'isAdmin': user.is_superuser,
        }
        response_data = {
            'token': token.key,
            **user_data
        }
        return Response(response_data)
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Access token authentication succeeded
        user = request.user
        # Process the authenticated user as needed
        print(user.country)
        if user is not None:
            try:
                loggedUser = get_object_or_404(User, username=user.username)
                serializer = UserSerializer(loggedUser)
                token, created = Token.objects.get_or_create(user=user)
            except Token.DoesNotExist:
                print('Token does not exist')
            return Response({'token': token.key , 'user': serializer.data })
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)