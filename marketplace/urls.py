from django.urls import path
from marketplace.views import MarketplaceView

urlpatterns = [
    path('', MarketplaceView.as_view(), name="marketplace"),
]