import os
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.middleware import csrf
from rest_framework import views
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase


def _extract_token_from_cookie(request):
    token = request.COOKIES.get('refresh')
    if not token:
        raise NotAuthenticated(detail=_('Refresh cookie not set. Try to authenticate first.'))
    else:
        request.data['refresh'] = token
    return request


class _TokenCookieViewMixin(TokenViewBase):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data)

        csrf.get_token(self.request)
        response = self.set_auth_cookies(response, serializer.validated_data)

        return response

    def set_auth_cookies(self, response, data):
        expires = self.get_refresh_token_expiration()

        if os.getenv('SERVER_TYPE') == 'dev' or not os.getenv('SERVER_TYPE'):
            response.set_cookie(
                'access', data['access'],
                expires=expires,
                httponly=True,
            )
            if 'refresh' in data:
                response.set_cookie(
                    'refresh', data['refresh'],
                    expires=expires,
                    httponly=True,
                )
        elif os.getenv('SERVER_TYPE') == 'prod':
            response.set_cookie(
                'access', data['access'],
                expires=expires,
                httponly=True,
                domain=settings.CSRF_COOKIE_DOMAIN,
                samesite='Lax',
                secure=True
            )
            if 'refresh' in data:
                response.set_cookie(
                    'refresh', data['refresh'],
                    expires=expires,
                    httponly=True,
                    domain=settings.CSRF_COOKIE_DOMAIN,
                    samesite='Lax',
                    secure=True
                )

        return response

    def get_refresh_token_expiration(self):
        return datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']


class CustomTokenObtainPairView(_TokenCookieViewMixin):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairSerializer


custom_token_obtain_pair = CustomTokenObtainPairView.as_view()


class CustomTokenRefreshView(_TokenCookieViewMixin):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        request = _extract_token_from_cookie(request)
        return super().post(request, *args, **kwargs)

    def get_refresh_token_expiration(self):
        token = RefreshToken(self.request.data['refresh'])
        return datetime.fromtimestamp(token.payload['exp'])


custom_token_refresh = CustomTokenRefreshView.as_view()


class TokenCookieDeleteView(views.APIView):
    """
    Deletes httpOnly auth cookies.
    Used as logout view while using AUTH_COOKIE
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        response = Response({})

        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response


custom_token_delete = TokenCookieDeleteView.as_view()
