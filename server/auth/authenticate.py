from django.contrib.auth import backends
from django.db.models import Q

from users.models import User
from users.serializers import UserSerializer


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


def jwt_response_payload_handler(token, user=None, request=None, *args):
    return {
        'token': token,
        'user': UserSerializer(user, many=False).data
    }