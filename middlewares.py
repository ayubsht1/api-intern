import logging
import traceback

logging.basicConfig(level=logging.DEBUG)


class ExceptionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code != 200:
                logging.debug(str(traceback.format_exc()))
        except Exception as e:
            logging.debug(str(e))
        return response