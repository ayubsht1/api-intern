from rest_framework.views import APIView
from django.http import JsonResponse

class UUEView(APIView):
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({"data": "UUE Response"})