from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.settings import api_settings
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from core.models import User
from songBank import settings
from rest_framework import status


class CustomTokenEncoder(Token):

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def for_user(cls, user):

        print('USER TOKEN CHECK')

        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[api_settings.TOKEN_USER_CLASS] = TokenUser

        return token


#     def __call__(self, token):
#         issued_at = datetime.utcnow()
#         expiration_time = issued_at + timedelta(seconds=self.lifetime)

#         user = token.user  # assuming the token object has a user property

#         payload = {
#             'user_id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'iat': issued_at,
#             'exp': expiration_time,
#         }

#         # add any additional data you want to include in the payload here

#         return super().__call__(payload)

#     @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
#     def authenticate_user(request):
#         try:
#             email = request.data['email']
#             password = request.data['password']
#             user = User.objects.get(email=email, password=password)

#             if user:
#                 try:
#                     payload = jwt_payload_handler(user)

#                     token = jwt.encode(payload, settings.SECRET_KEY)

#                     user_details = {}

#                     user_details['name'] = "%s %s" % (

#                     user.first_name, user.last_name)

#                     user_details['token'] = token

#                     user_logged_in.send(sender=user.__class__,

#                                             request=request, user=user)

#                     return Response(user_details, status=status.HTTP_200_OK)

#                 except Exception as e:

#                         raise e

#             else:

#                 res = {

#                         'error': 'can not authenticate with the given credentials or the account has been deactivated'}

#                 return Response(res, status=status.HTTP_403_FORBIDDEN)

#         except KeyError:

#             res = {'error': 'please provide a email and a password'}

#         return Response(res)


# @classmethod
#     def for_user(cls, user):
#         """
#         Returns an authorization token for the given user that will be provided
#         after authenticating the user's credentials.
#         """
#         user_id = getattr(user, api_settings.USER_ID_FIELD)
#         if not isinstance(user_id, int):
#             user_id = str(user_id)

#         token = cls()
#         token[api_settings.TOKEN_USER_CLASS] = TokenUser

#         return token
