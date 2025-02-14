from typing import Optional, Set, Tuple, TypeVar

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, authentication
from rest_framework.request import Request

from rest_framework_simplejwt.exceptions import (
    TokenError,
)
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import get_md5_hash_password
from authentication.models import UserJWT
from rest_framework.exceptions import bad_request
from django.http import JsonResponse
from response import unauthorized_access

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES: Set[bytes] = {
    h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES
}

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

DEFAULT_ERROR_CODE = 401

def unauthorized(message):
    return unauthorized_access(error_message=message)

class JWTAuthentication(authentication.BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        
        user = self.get_user(validated_token)
        try:
            user_jwt = UserJWT.objects.filter(user=user).filter(access_token=raw_token.decode()).first()
            # if not user_jwt:
            #     return unauthorized("Session Expired, Please Re-Login.")
            # if not user_jwt.is_authenticated:
            #     return unauthorized("Session Expired, Please Re-Login.")
            # token = user_jwt.access_token
            # if not token == raw_token.decode():
            #     return unauthorized("Session Expired, Please Re-Login.")
            if not user_jwt:
                return unauthorized("Session Expired, Please Re-Login.")
        except:
            return unauthorized("Session Expired, Please Re-Login.")

        return self.get_user(validated_token), validated_token

    def authenticate_header(self, request: Request) -> str:
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get_header(self, request: Request) -> bytes:
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get(api_settings.AUTH_HEADER_NAME)

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header: bytes) -> Optional[bytes]:
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            # raise AuthenticationFailed(
            #     _("Authorization header must contain two space-delimited values"),
            #     code="bad_authorization_header",
            # )
            return unauthorized("Invalid Authentication Token.")

        return parts[1]

    def get_validated_token(self, raw_token: bytes) -> Token:
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        # raise InvalidToken(
        #     {
        #         "detail": _("Given token not valid for any token type"),
        #         "messages": messages,
        #     }
        # )
        return unauthorized("Token Expired")

    def get_user(self, validated_token: Token) -> AuthUser:
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            # raise InvalidToken(_("Token contained no recognizable user identification"))
            return unauthorized("Invalid Token.")

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            # raise AuthenticationFailed(_("User not found"), code="user_not_found")
            return unauthorized("User Not Found.")

        if not user.is_active:
            # raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
            return unauthorized("Your account is currently disabled.")

        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(
                api_settings.REVOKE_TOKEN_CLAIM
            ) != get_md5_hash_password(user.password):
                # raise AuthenticationFailed(
                #     _("The user's password has been changed."), code="password_changed"
                # )
                return unauthorized("Something went wrong, Please Try Again.")

        return user