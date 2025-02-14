from django.urls import path
from authentication.user.views import UserLoginView
from authentication.views import RegisterApi, LogoutApi

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', LogoutApi.as_view()),
]