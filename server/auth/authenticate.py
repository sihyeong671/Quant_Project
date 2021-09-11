import datetime, jwt

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth import backends
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings

from users.utils import user_record_login


User = get_user_model()


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        
        if not authorization_header:
            return None
            
        try:
            prefix = authorization_header.split(' ')[0]
            if prefix.lower() != 'jwt':
                raise exceptions.AuthenticationFailed('Token is not jwt')

            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        
        user = User.objects.filter(id=payload['user_id']).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')
        
        self.enforce_csrf(request)
        return (user, None)


    def enforce_csrf(self, request):
        check = CSRFCheck()
        
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')


class AdministratorAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        
        if not authorization_header:
            return None
            
        try:
            prefix = authorization_header.split(' ')[0]
            if prefix.lower() != 'jwt':
                raise exceptions.AuthenticationFailed('Token is not jwt')

            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        
        user = User.objects.filter(id=payload['user_id']).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.is_superuser:
            raise exceptions.AuthenticationFailed('User is not superuser')
        
        self.enforce_csrf(request)
        return (user, None)


    def enforce_csrf(self, request):
        check = CSRFCheck()
        
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')


class EmailorUsernameAuthBackend(backends.ModelBackend):
    def authenticate(self, username, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )
            if user.check_password(password):
                return user
        except:
            return None
    
    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None;


def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=0, minutes=5
        ),
        'iat': datetime.datetime.utcnow(),
    }
    
    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY, algorithm='HS256'
    ).decode('utf-8')
    
    return access_token
    
    
def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    
    refresh_token = jwt.encode(
        refresh_token_payload, 
        settings.REFRESH_TOKEN_SECRET, algorithm='HS256'
    ).decode('utf-8')
    
    return refresh_token


def jwt_login(response, user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
    data = {
        'access_token': access_token,
    }
    
    response.data = data
    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    
    user_record_login(user)
    
    return response
    