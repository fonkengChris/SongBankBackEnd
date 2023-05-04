# from .models import User
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
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

    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop('email', None)
        self.password = kwargs.pop('password', None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user data to the token payload
        data['email'] = self.user.email

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
        email = kwargs.get('email', self.email)
        password = kwargs.get('password', self.password)

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validators])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
