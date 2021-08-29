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


class GoogleLoginApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        app_key = settings.GOOGLE_OAUTH2_CLIENT_ID
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"
        # scope = " ".join(scope)
        
        redirect_uri = settings.BASE_BACKEND_URL + "/api/v1/auth/login/google/callback"
        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
        
        response = redirect(
            f"{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
        )
        
        print(response)
        
        return response


class GoogleSigninCallBackApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        google_token_api = "https://oauth2.googleapis.com/token"
        
        
        
        access_token = google_get_access_token(google_token_api, code)
        user_data = google_get_user_info(access_token=access_token)
        
        print(user_data)
        
        profile_data = {
            'username': user_data['email'],
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
            'nickname': user_data.get('nickname', ''),
            'name': user_data.get('name', ''),
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


class NaverLoginApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        app_key = settings.NAVER_OAUTH2_CLIENT_ID
        state = "RAMDOM_STATE"
        redirect_uri = settings.BASE_BACKEND_URL + "/api/v1/auth/login/naver/callback"
        naver_auth_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
        
        response = redirect(
            f"{naver_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}&state={state}"
        )
        
        return response


class NaverSigninCallBackApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        app_key = settings.NAVER_OAUTH2_CLIENT_ID
        app_secret_key = settings.NAVER_OAUTH2_CLIENT_SECRET
        auth_code = request.GET.get('code')
        state = request.GET.get('state')
        naver_token_api = "https://nid.naver.com/oauth2.0/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': app_key,
            'client_secret': app_secret_key,
            'state': state,
            'code': auth_code,
        }
        
        access_token, token_type = naver_get_access_token(naver_token_api, data)
        user_info = naver_get_user_info(access_token, token_type)
        
        print(user_info)
        
        profile_data = {
            'username': user_info['response'].get('email'),
            'image': user_info['response'].get('profile_image', ''),
            'nickname': user_info['response'].get('nickname', ''),
            'name': user_info['response'].get('name', ''),
            'path': "naver",
            
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
    