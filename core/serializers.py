# from .models import User
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'password', 'email',
                  'date_joined', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __call__(self, *args, **kwargs):
        print('CustomTokenObtainPairSerializer called')
        return super().__call__(*args, **kwargs)
    """
    Custom token serializer that includes additional user data in the token payload.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user data to the token payload
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom user data to the access token payload
        token['user_id'] = user.id
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

    def authenticate(self, request, **kwargs):
        """
        Authenticate the user based on the request data.
        """
        email = kwargs.get('email', None)
        password = kwargs.get('password', None)

        if not email or not password:
            return None

        # Lookup the user by email address
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # Check if the password is valid
        if not user.check_password(password):
            return None

        # Return the authenticated user
        return user
