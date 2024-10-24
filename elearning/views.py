from rest_framework.views import APIView
from django.http import JsonResponse

class ElearningView(APIView):
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({"data": "Elearning Response"})