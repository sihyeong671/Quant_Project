from django.urls import path, include

from auth.apis import LoginApi, LogoutApi, username_duplicate_checkApi, email_duplicate_checkApi, RefreshJWTtoken
from auth.googleapi import *
from auth.kakaoapi import *
from auth.naverapi import *


login_patterns = [
    path('refresh', RefreshJWTtoken.as_view()),
    path('', LoginApi.as_view(), name='login'),
    
    path('google', GoogleLoginApi.as_view(), name='google_login'),
    path('google/callback', GoogleSigninCallBackApi.as_view(), name='google_login_callback'),
    
    path('kakao', KakaoLoginApi.as_view(), name='kakao_login'),
    path('kakao/callback', KakaoSigninCallBackApi.as_view(), name='kakao_login_callback'),
    
    path('naver', NaverLoginApi.as_view(), name='naver_login'),
    path('naver/callback', NaverSigninCallBackApi.as_view(), name='naver_login_callback'),
    
]

validate_patterns = [
    path('username/', username_duplicate_checkApi.as_view()),
    path('email/', email_duplicate_checkApi.as_view()),
    
]

urlpatterns = [
    path('logout', LogoutApi.as_view(), name="logout"),
    path('login/', include(login_patterns)),
    path('validate/', include(validate_patterns)),
]

