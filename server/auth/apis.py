from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebTokenView

from django.conf import settings
from django.core.exceptions import ValidationError

from auth.authenticate import CustomJSONWebTokenAPIView
from api.mixins import PublicApiMixin, ApiAuthMixin
from users.utils import user_record_login, user_change_secret_key


User = get_user_model()


class LoginApi(PublicApiMixin, CustomJSONWebTokenAPIView):
    """
    Using Custom LoginApi rather than obtain_jwt_token
    Because have to record last login time
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user') or request.user
        user_record_login(user=user)

        return super().post(request, *args, **kwargs)


class LogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        """
        Logs out user by removing JWT cookie header.
        """
        user_change_secret_key(user=request.user)

        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])

        return response

class username_duplicate_checkApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        input_username = request.data.get('username', '')
        
        if not input_username:
            raise ValidationError("Need username")
        
        user = User.objects.filter(username=input_username).first()
        
        if user:
            raise ValidationError("There is an ID registered with that username")
        
        return Response({
            "message": "Allowed username"
        }
        ,status=status.HTTP_200_OK)


class email_duplicate_checkApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        input_email = request.data.get('email', '')
        
        if not input_email:
            raise ValidationError("Need email")
        
        user = User.objects.filter(email=input_email).first()
        
        if user:
            raise ValidationError("There is an ID registered with that email")
        
        return Response({
            "message": "Allowed email"
        }
        ,status=status.HTTP_200_OK)
