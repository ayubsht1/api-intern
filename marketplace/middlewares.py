from django.http import JsonResponse

class UrlsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response= self.get_response(request)
            if response.status_code == 404:
                return JsonResponse({
                    'error_message':'The requested URL was not found on the server.'
                }, status=404)
        except Exception as e:
            return JsonResponse({
                'error_message':'Something went wrong.'
            },status=500)
        return response

class InternalServerMiddleware:
    def __init__(self, get_response):
        self.get_response= get_response

    def __call__(self, request):
        try:
            response= self.get_response(request)
            if response.status_code == 500:
                return JsonResponse({
                    'error_message':'Server Error'
                },status= 500)
        except Exception as e:
            return JsonResponse({
                'error_message':'internal server error'
            }, status= 500)
        return response
    