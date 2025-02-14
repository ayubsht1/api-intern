from authentication.views import LoginApi
from authentication.serializers import LoginSerializer


class UserLoginView(LoginApi):
    USER_ROLE = "User"
    USERNAME_FIELD = "email"
    login_serializer = LoginSerializer