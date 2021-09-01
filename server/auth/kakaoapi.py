from rest_framework.views import APIView

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model

from api.mixins import PublicApiMixin
from users.utils import user_get_or_create
from auth.services import kakao_get_access_token, kakao_get_user_info
from auth.authenticate import jwt_login


# User = settings.AUTH_USER_MODEL
User = get_user_model()


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
    