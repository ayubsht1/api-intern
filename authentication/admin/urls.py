from django.urls import path
from authentication.admin.views import AdminLoginView, AdminRegisterView

urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view()),
    path('admin/login/', AdminLoginView.as_view()),
    # path('logout/', LogoutApi.as_view()),
]