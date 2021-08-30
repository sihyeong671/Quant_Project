from urllib.parse import urlencode
from django.http.response import HttpResponse

from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebTokenView

from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import ValidationError
from django.conf import settings

from api.mixins import PublicApiMixin, ApiAuthMixin
from users.utils import \
    user_record_login, user_change_secret_key, user_get_or_create

from auth.services import \
    jwt_login, google_get_access_token, \
    google_get_user_info, kakao_get_access_token, \
    kakao_get_user_info, naver_get_access_token, \
    naver_get_user_info


User = settings.AUTH_USER_MODEL


class LoginApi(PublicApiMixin, ObtainJSONWebTokenView):
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
    