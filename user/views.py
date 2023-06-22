from rest_framework import generics
from django.shortcuts import get_object_or_404, render
from .serializers import UserSerializer
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
            print(user)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAdminOrUnauthenticatedUser]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')

        # Validate the password
        try:
            validate_password(password)
        except ValidationError as e:
            serializer.fail('password_validation', password_validators=e.error_list)

        # Save the user
        serializer.save(password=password, is_active=True)


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
    
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                token, created = Token.objects.get_or_create(user=user)
            except Token.DoesNotExist:
                print('Token does not exist')
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)
        
        

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
