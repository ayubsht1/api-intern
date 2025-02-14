from rest_framework.views import APIView
from rest_framework import permissions
from authentication.serializers import RegisterSerializer, LoginSerializer
from authentication.models import User, UserJWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.conf import settings
from response import validation_error, bad_request, json_resp
from utils import base_encoder


JWT_CONFIG = {}
AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"

try:
    JWT_CONFIG = settings.SIMPLE_JWT
    AUTH_HEADER_NAME = JWT_CONFIG.get("AUTH_HEADER_NAME") if JWT_CONFIG else "HTTP_AUTHORIZATION"
except:
    pass


class RegisterApi(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    USER_TYPE = "User"
    model_class = User
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            raise validation_error(serializer.errors)
        validated_data = serializer.validated_data
        validated_data.pop("confirm_password")
        validated_data['user_type'] = self.USER_TYPE
        validated_data['username'] = base_encoder(validated_data["phone"])
        self.model_class.objects.create_user(**validated_data)
        return json_resp(data={"message": "Success"})
        
        
class LoginApi(TokenObtainPairView):
    DEFAULT_ERROR_MESSAGE = "Invalid Username or Password."
    login_serializer = LoginSerializer
    USER_ROLE = None
    USERNAME_FIELD = None
    
    def _validate_user_role(self, user):
        if not self.USER_ROLE:
            raise bad_request("Something went wrong.")
        if not user.user_type == self.USER_ROLE:
            raise bad_request("Could't login.")
        return user
    
    def post(self, request, *args, **kwargs):
        serializer = self.login_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            raise validation_error(error_messages=serializer.errors)
        
        try:
            email = request.data.pop("email")
            request.data[self.USERNAME_FIELD] = email
            token = super().post(request, *args, **kwargs)
        except Exception as e:
            return bad_request(error_message=self.DEFAULT_ERROR_MESSAGE)
        
        user = self._validate_user_role(authenticate(**request.data))
        
        data = {
            "access_token": token.data["access"],
            "refresh_token": token.data["refresh"]
        }
        jwt_log = data.copy()
        jwt_log.update({
            "user": user,
        })
        user_jwt = UserJWT.objects.filter(user=jwt_log['user']).first()
        if not user_jwt:
            UserJWT.objects.create(**jwt_log)
        else:
            user_jwt.update_token(**jwt_log)
        return json_resp(data=data)


class LogoutApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        auth_header = request.META.get(AUTH_HEADER_NAME)
        token = auth_header.split()[1]
        try:
            user_jwt = UserJWT.objects.get(access_token=token)
            user_jwt.remove_token()
        except UserJWT.DoesNotExist:
            pass
        return json_resp({"message": "Logout Successful."})


class RefreshTokenApi(TokenRefreshView):
    permission_classes = [permissions.AllowAny]