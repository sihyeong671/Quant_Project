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
    kakao_get_user_info


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


class GoogleLoginApi(PublicApiMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        domain = settings.BASE_BACKEND_URL
        api_uri = reverse('api:v1:auth:google_login')
        redirect_uri = f'{domain}{api_uri}'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)
        
        profile_data = {
            'username': user_data['email'],
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
            'image': user_data.get('picture', None),
            'path': "google",
            
        }

        user, _ = user_get_or_create(**profile_data)

        response = redirect(settings.BASE_FRONTEND_URL)
        response = jwt_login(response=response, user=user)

        return response


class KakaoLoginApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        app_key = settings.KAKAO_REST_API_KEY
        redirect_uri = settings.BASE_BACKEND_URL + "/api/v1/auth/login/kakao/callback"
        kakao_auth_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        scopes = "&scope=account_email, profile_image, profile_nickname"
        
        response = redirect(
            f"{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}" +
            scopes
        )
        
        return response


class KakaoSigninCallBackApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirection_uri': settings.BASE_BACKEND_URL + "/api/v1/auth/login/kakao/callback",
            'code': auth_code,
        }
        
        access_token = kakao_get_access_token(kakao_token_api, data)
        user_info = kakao_get_user_info(access_token)
        
        profile_data = {
            'username': user_info['kakao_account'].get('email'),
            'image': user_info['kakao_account'].get('profile_image', ''),
            'nickname': user_info['kakao_account'].get('profile_nickname', ''),
            'path': "kakao",
            
        }
        
        user, _ = user_get_or_create(**profile_data)
        
        response = redirect(settings.BASE_FRONTEND_URL)
        response = jwt_login(response=response, user=user)
        
        return response


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
    