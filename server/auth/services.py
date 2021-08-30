import requests
from typing import Dict, Any

from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import set_cookie_with_token

from users.models import User
from users.utils import user_record_login


GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def jwt_login(response, user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    if api_settings.JWT_AUTH_COOKIE:
        set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

    user_record_login(user=user)

    return response


def google_get_access_token(google_token_api, code):
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    code = code
    grant_type = 'authorization_code'
    redirection_uri = settings.BASE_BACKEND_URL + "/api/v1/auth/login/google/callback"
    state = "random_string"
    
    google_token_api += \
        f"?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirection_uri}&state={state}"
    
    token_response = requests.post(google_token_api)
    
    if not token_response.ok:
        raise ValidationError('google_token is invalid')
    
    access_token = token_response.json().get('access_token')
    
    return access_token


def google_get_user_info(*, access_token: str):
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        params={
            'access_token': access_token
        }
    )

    if not user_info_response.ok:
        raise ValidationError('Failed to obtain user info from Google.')
    
    user_info = user_info_response.json()
    
    return user_info


def kakao_get_access_token(kakao_token_api, data):
    token_response = requests.post(kakao_token_api, data=data)
    
    if not token_response.ok:
        raise ValidationError('kakao_token is invalid')
    
    access_token = token_response.json().get('access_token')
    
    return access_token


def kakao_get_user_info(access_token):
    user_info_response = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"Bearer ${access_token}"
        }
    )
    
    if not user_info_response.ok:
        raise ValidationError('Failed to obtain user info from Kakao')
    
    user_info = user_info_response.json()
    
    return user_info
    

def naver_get_access_token(naver_token_api, data):
    token_response = requests.post(naver_token_api, data=data)
    
    if not token_response.ok:
        raise ValidationError('naver_token is invalid')
    
    access_token = token_response.json().get('access_token')
    token_type = token_response.json().get('token_type')
    
    return access_token, token_type


def naver_get_user_info(access_token, token_type='Bearer'):
    user_info_response = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={
            "Authorization": f"{token_type} {access_token}"
        }
    )
    
    if not user_info_response.ok:
        raise ValidationError('Failed to obtain user info from Naver')
    
    user_info = user_info_response.json()
    
    return user_info
    