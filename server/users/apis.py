from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.management.utils import get_random_secret_key
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from api.mixins import ApiAuthMixin, PublicApiMixin

from auth.services import jwt_login

from users.serializers import RegisterSerializer, UserSerializer, PasswordChangeSerializer
from users.models import Profile, User
from users.services import send_mail, email_auth_string


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user, context={'request':request}).data)
    
    def put(self, request, *args, **kwargs):
        user = request.user

        if not check_password(request.data.get("oldpassword"), user.password):
            raise serializers.ValidationError(
                _("passwords do not match")
            )
        
        serializer = PasswordChangeSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        else:
            validated_data = serializer.validated_data
            serializer.update(user=user, validated_data=validated_data)
            return Response({
                "message": "Change password success"
                }, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        path = user.profile.path
        
        if path == "kakao" or path == "google":
            user.delete()
            return Response({
                "message": "Delete user success"
                }, status=status.HTTP_204_NO_CONTENT)
            
        if not check_password(request.data.get("password"), user.password):
            raise serializers.ValidationError(
                _("passwords do not match")
            )
            
        user.delete()
        
        return Response({
            "message": "Delete user success"
            }, status=status.HTTP_204_NO_CONTENT)


class UserCreateApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({
                "message": "Request Body Error"
                }, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        profile = Profile(user=user, introduce="hello")
        profile.save()
        
        response = redirect(settings.BASE_FRONTEND_URL)
        response = jwt_login(response=response, user=user)
        return response


class FindIDApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        target_email = request.data.get('email', '')
        user = User.objects.get(email=target_email)
        
        data = {
            "id": user.username
        }
        
        return Response(data, status=status.HTTP_200_OK)


class SendPasswordEmailApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        target_username = request.data.get('username', '')
        target_email = request.data.get('email', '')
        
        target_user = User.objects.get(
            username=target_username, 
            email=target_email
        )
        
        if target_user:
            auth_string = email_auth_string()
            target_user.profile.auth = auth_string
            target_user.profile.save()
            
            send_mail(
                '[PROJECT:QUANT] 비밀번호 찾기 인증 메일입니다.',
                recipient_list=[target_email],
                html=render_to_string('recovery_email.html', {
                    'auth_string': auth_string,
                })
            )
            return Response({
                "message": "Verification code sent"
            }, status=status.HTTP_200_OK)
            
        else:
            return Response({
                "message": "User does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
            

class ConfirmPasswordEmailApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwagrs):
        target_username = request.data.get('username', '')
        target_code = request.data.get('code', '')
        user = User.objects.get(username=target_username)
        profile = user.profile
        
        if profile.auth == target_code:
            profile.auth = get_random_secret_key()
            profile.save()
            
            response = Response({
                "message": "Verification success",
                "user": target_username,
            }, status=status.HTTP_202_ACCEPTED)
            response = jwt_login(response=response, user=user)
            return response
        else:
            return Response({
                "message": "Verification Failed"
            }, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        password1 = request.data.get('password1', '')
        password2 = request.data.get('password2', '')
        user = request.user
        
        if password1 != password2 or not password1 or not password2:
            raise ValidationError(_("password error"))
        
        user.set_password(password1)
        user.save()
        
        response = Response({
            "message": "Reset password success! Go to login page"
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])

        return response