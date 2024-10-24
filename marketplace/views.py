from rest_framework.views import APIView
from django.http import JsonResponse

class MarketplaceView(APIView):
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({"data": "Marketplace Response"})