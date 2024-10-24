from django.urls import path
from ebooks.views import EbookView

urlpatterns = [
    path('', EbookView.as_view(), name="ebook"),
]