from rest_framework.views import APIView

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import get_user_model

from api.mixins import PublicApiMixin
from users.utils import user_get_or_create
from auth.services import google_get_access_token, google_get_user_info
from auth.authenticate import jwt_login


User = get_user_model()


class GoogleLoginApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        app_key = settings.GOOGLE_OAUTH2_CLIENT_ID
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"
        
        redirect_uri = settings.BASE_BACKEND_URL + "/api/v1/auth/login/google/callback"
        google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
        
        response = redirect(
            f"{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
        )
        
        return response


class GoogleSigninCallBackApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        google_token_api = "https://oauth2.googleapis.com/token"
        
        access_token = google_get_access_token(google_token_api, code)
        user_data = google_get_user_info(access_token=access_token)
        
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
    