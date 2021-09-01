from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from auth.authenticate import SafeJWTAuthentication


class ApiAuthMixin:
    authentication_classes = (SafeJWTAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )


class PublicApiMixin:
    authentication_classes = ()
    permission_classes = ()
