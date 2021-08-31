from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshAuthTokenSerializer
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import backends
from django.db.models import Q
from django.contrib.auth import get_user_model

# from users.models import User
from users.serializers import UserSerializer

from auth.services import my_set_cookie_with_token

User = get_user_model()

class EmailorUsernameAuthBackend(backends.ModelBackend):
    def authenticate(self, username, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )
            if user.check_password(password):
                return user
        except:
            return None
    
    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None;


class CustomJSONWebTokenAPIView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user') or request.user
        token = serializer.validated_data.get('token')
        issued_at = serializer.validated_data.get('issued_at')
        response_data = JSONWebTokenAuthentication. \
            jwt_create_response_payload(token, user, request, issued_at)

        response = Response(response_data, status=status.HTTP_201_CREATED)

        if api_settings.JWT_AUTH_COOKIE:
            my_set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

        return response


class CustomRefreshJSONWebTokenAPIView(CustomJSONWebTokenAPIView):
    serializer_class = RefreshAuthTokenSerializer
    

def jwt_response_payload_handler(token, user=None, request=None, *args):
    return {
        'token': token,
        'user': UserSerializer(user, many=False).data
    }