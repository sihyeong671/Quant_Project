import jwt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from auth.authenticate import generate_access_token, jwt_login
from api.mixins import PublicApiMixin, ApiAuthMixin
from users.utils import user_record_login, user_change_secret_key
from django.utils.decorators import method_decorator


User = get_user_model()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        user = User
        username = request.data.get('username')
        password = request.data.get('password')
        
        if (username is None) or (password is None):
            return Response({
                "message": "username/password required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({
                "message": "user not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response({
                "message": "wrong password"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response(status=status.HTTP_200_OK)
        return jwt_login(response, user)
        

@method_decorator(csrf_protect, name='dispatch')
class RefreshJWTtoken(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refreshtoken')
        
        if refresh_token is None:
            return Response({
                "message": "Authentication credentials were not provided."
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256']
            )
        except:
            return Response({
                "message": "expired refresh token, please login again."
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.filter(id=payload['user_id']).first()
        
        if user is None:
            return Response({
                "message": "user not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({
                "message": "user is inactive"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = generate_access_token(user)
        
        return Response(
            {
                'access_token': access_token,
            }
        )
        
        
@method_decorator(csrf_protect, name='dispatch')
class LogoutApi(PublicApiMixin, APIView):
    def post(self, request):
        
        user_change_secret_key(request.user)
        
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refreshtoken')

        return response


@method_decorator(csrf_protect, name='dispatch')
class username_duplicate_checkApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        input_username = request.data.get('username', '')
        
        if not input_username:
            raise ValidationError("Need username")
        
        user = User.objects.filter(username=input_username).first()
        
        if user:
            raise ValidationError("There is an ID registered with that username")
        
        return Response({
            "message": "Allowed username"
        }
        ,status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class email_duplicate_checkApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        input_email = request.data.get('email', '')
        
        if not input_email:
            raise ValidationError("Need email")
        
        user = User.objects.filter(email=input_email).first()
        
        if user:
            raise ValidationError("There is an ID registered with that email")
        
        return Response({
            "message": "Allowed email"
        }
        ,status=status.HTTP_200_OK)
