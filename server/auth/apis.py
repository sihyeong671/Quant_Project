from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebTokenView

from django.conf import settings
from django.core.exceptions import ValidationError

from auth.authenticate import CustomJSONWebTokenAPIView
from api.mixins import PublicApiMixin, ApiAuthMixin
from users.utils import user_record_login, user_change_secret_key


User = settings.AUTH_USER_MODEL


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


def username_duplicate_check(request):
    input_username = request.GET.get('username', '')
    
    user = User.objects.filter(username=input_username).first()
    
    if user:
        raise ValidationError("There is an ID registered with that username")
    
    return HttpResponse(status=status.HTTP_200_OK)


def email_duplicate_check(request):
    input_email = request.GET.get('email', '')
    
    user = User.objects.filter(username=input_email).first()
    
    if user:
        raise ValidationError("There is an ID registered with that email")
    
    return HttpResponse(status=status.HTTP_200_OK)
    