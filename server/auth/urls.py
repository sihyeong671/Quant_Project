from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from django.urls import path, include

from auth.apis import \
    LoginApi, GoogleLoginApi, LogoutApi, KakaoLoginApi, \
    KakaoSigninCallBackApi, username_duplicate_check, \
    email_duplicate_check


login_patterns = [
    path('verify', verify_jwt_token),
    path('refresh', refresh_jwt_token),
    path('', LoginApi.as_view(), name='login'),
    path('google', GoogleLoginApi.as_view(), name='google_login'),
    path('kakao', KakaoLoginApi.as_view(), name='kakao_login'),
    path('kakao/callback', KakaoSigninCallBackApi.as_view(), name='kakao_login_callback'),
    
]

validate_patterns = [
    path('username/', username_duplicate_check),
    path('email/', email_duplicate_check),
    
]

urlpatterns = [
    path('logout', LogoutApi.as_view(), name="logout"),
    path('login/', include(login_patterns)),
    path('validate/', include(validate_patterns)),
]

