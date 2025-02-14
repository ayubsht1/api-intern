from authentication.views import LoginApi, RegisterApi


class AdminLoginView(LoginApi):
    USER_ROLE = "Admin"
    USERNAME_FIELD = "email"
    
    
class AdminRegisterView(RegisterApi):
    USER_TYPE = "Admin"