# from django.shortcuts import render
# from django.contrib.auth.signals import user_logged_in
# from rest_framework import status
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.permissions import AllowAny
# from rest_framework_jwt.utils import jwt_payload_handler
# import jwt
# from core.models import User
# from core.serializers import CustomTokenObtainPairSerializer, UserCreateSerializer, UserSerializer
# from songBank import settings


# class CreateUserViewset(ModelViewSet):

#     # Allow any user (authenticated or not) to access this url

#     permission_classes = (AllowAny,)
#     serializer_class = CustomTokenObtainPairSerializer
#     queryset = User.objects.all()

#     def post(self, request, *args, **kwargs):

#         user = request.data
#         serializer = UserCreateSerializer(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from core.models import User
from core.serializers import CustomTokenObtainPairSerializer, UserCreateSerializer, UserSerializer
from songBank import settings
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUserViewset(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # Generate the token using CustomTokenObtainPairSerializer
        token_serializer = CustomTokenObtainPairSerializer(data={
            'email': serializer.data['email'],
            'password': request.data.get('password')
        })

        if token_serializer.is_valid():
            # Return the token and user data in the response
            response_data = {
                'token': token_serializer.validated_data['access'],
                'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = UserCreateSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
