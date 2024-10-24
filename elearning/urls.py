from django.urls import path
from elearning.views import ElearningView

urlpatterns = [
    path('', ElearningView.as_view(), name="elearning"),
]