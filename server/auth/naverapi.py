from rest_framework.views import APIView

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model


from api.mixins import PublicApiMixin
from users.utils import user_get_or_create
from auth.services import jwt_login, naver_get_access_token, naver_get_user_info
    

# User = settings.AUTH_USER_MODEL
User = get_user_model()


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
    