from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ApiAuthMixin:
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class PublicApiMixin:
    authentication_classes = ()
    permission_classes = ()
