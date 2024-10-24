from django.urls import path
from uue.views import UUEView

urlpatterns = [
    path('', UUEView.as_view(), name="uue"),
]