from tokenize import TokenError
from rest_framework.permissions import IsAuthenticated
from core.serializers import CustomTokenObtainPairSerializer


class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        print(request.META)

        if not super().has_permission(request, view):
            return False

        # Get the token from the request headers
        token = request.META.get('Authorization', '').split(' ')[1]

        # Decode the token using the CustomTokenPairSerializer class
        try:
            decoded_token = CustomTokenObtainPairSerializer().validate(token)
        except TokenError as e:
            return False

        # Add the decoded token to the request for later use
        request.auth = decoded_token

        # Return True to indicate that the user is authenticated and authorized to access the view
        return True
