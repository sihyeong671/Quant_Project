from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction
from django.db.models import Q, F
from django.conf import settings
from django.core import exceptions
from django.contrib.auth.hashers import check_password
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from api.mixins import ApiAuthMixin, PublicApiMixin

from auth.authenticate import jwt_login


from users.serializers import RegisterSerializer, UserSerializer,\
    PasswordChangeSerializer, validate_password12
from users.models import Profile
from users.services import send_mail, email_auth_string

BASE_DIR = settings.BASE_DIR
User = get_user_model()


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        if request.user is None:
            raise exceptions.PermissionDenied('PermissionDenied')
        
        username = request.user.username
        
        user_query = User.objects\
            .prefetch_related(
                'profile__favorite_post',
                'profile__favorite_post__favorite_user',
                'profile__favorite_post__creator',
                'profile__favorite_post__category',
                'profile__favorite_category',
                'profile__favorite_category__favorite_user',
                'profile__favorite_company',
                'custom_bs',
            )\
            .filter(Q(username=username))
            
        data = UserSerializer(user_query, many=True, context={'request':request}).data
        
        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        if not check_password(request.data.get("oldpassword"), user.password):
            raise serializers.ValidationError(
                _("passwords do not match")
            )
        
        serializer = PasswordChangeSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        
        
        validated_data = serializer.validated_data
        print(validated_data)
        serializer.update(user=user, validated_data=validated_data)
        return Response({
            "message": "Change password success"
            }, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        signup_path = user.profile.signup_path
        
        if signup_path == "kakao" or signup_path == "google":
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
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({
                "message": "Request Body Error"
                }, status=status.HTTP_409_CONFLICT)

        user = serializer.save()
        
        profile = Profile(user=user, nickname=user.username, introduce="소개를 작성해주세요.")
        profile.save()
        
        response = Response(status=status.HTTP_200_OK)
        response = jwt_login(response=response, user=user)
        return response


class FindIDApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        target_email = request.data.get('email', '')
        user = User.objects.get(email=target_email)
        
        data = {
            "username": user.username
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
                'QUANTmanager 비밀번호 찾기 인증 메일입니다.',
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
        
        newpassword = validate_password12(password1, password2)
        
        user.set_password(password1)
        user.save()
        
        response = Response({
            "message": "Reset password success! Go to login page"
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])

        return response

