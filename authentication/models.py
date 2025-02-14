from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


USER_TYPE = [
    ("Admin", "Admin"),
    ("User", "User"),
    ("SuperUser", "SuperUser")
]


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)    
    phone = models.CharField(max_length=12, unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]



class UserJWT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    
    @property
    def user_role(self):
        return self.user.user_type
    
    @property
    def is_authenticated(self):
        return self.access_token != None
    
    def verify_token(self, token, type="access_token"):
        return getattr(self, type) == token
    
    def update_token(self, access_token=None, refresh_token=None, *args, **kwargs):
        if access_token:
            self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        self.save()
    
    def remove_token(self):
        self.access_token = None
        self.refresh_token = None
        self.save()