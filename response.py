from django.http import JsonResponse
from exceptions import ValidationException, BadRequestException, UnauthorizedException
from constants import SUCCESS_CODE


SUCCESS_STATUS_CODE = 200


def json_resp(data={}, meta={}):
    resp_data = {
        "code": SUCCESS_CODE,
        "data": data,
        "meta": meta
    }
    return JsonResponse(data=resp_data, status=SUCCESS_STATUS_CODE)


def validation_error(error_messages):
    raise ValidationException(detail=error_messages)

def bad_request(error_message):
    raise BadRequestException(detail=error_message)

def unauthorized_access(error_message="User not found."):
    raise UnauthorizedException(detail=error_message)