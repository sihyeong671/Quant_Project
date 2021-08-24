from django.urls import path

from users.apis import \
    UserMeApi, FindIDApi, SendPasswordEmailApi, \
    ResetPasswordApi, ConfirmPasswordEmailApi, UserCreateApi


urlpatterns = [
    path('me', UserMeApi.as_view(), name="me"),
    path('me/', UserCreateApi.as_view(), name="createuser"),
    path('me/id', FindIDApi.as_view(), name="findid"),
    path('password/code', SendPasswordEmailApi.as_view(), name="sendpw"),
    path('password/verifycode', ConfirmPasswordEmailApi.as_view(), name="confirmpw"),
    path('password/reset', ResetPasswordApi.as_view(), name="resetpw"),
    
]
