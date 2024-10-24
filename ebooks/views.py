from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

class EbookView(APIView):
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({"data": "Ebook Response"})