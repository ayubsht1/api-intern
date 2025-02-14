from django.urls import path
# from authentication.views import RegisterApi, LoginApi, LogoutApi

# urlpatterns = [
#     path('register/', RegisterApi.as_view()),
#     path('login/', LoginApi.as_view()),
#     path('logout/', LogoutApi.as_view()),
# ]

from authentication.admin.urls import urlpatterns as admin_urls
from authentication.user.urls import urlpatterns as user_urls

urlpatterns = []

urlpatterns.extend(user_urls)
urlpatterns.extend(admin_urls)