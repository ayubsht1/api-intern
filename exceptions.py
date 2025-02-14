from rest_framework.exceptions import APIException
from constants import BAD_REQUEST, VALIDATION_ERROR_CODE, UNAUTHORIZED_ACCESS

BAD_REQUEST_STATUS_CODE = 400
UNAUTHORIZED_STATUS_CODE = 401

class BaseException(APIException):
    status_code = 500
    

class ValidationException(BaseException):
    
    def __init__(self, detail=None, status_code=BAD_REQUEST_STATUS_CODE, code=VALIDATION_ERROR_CODE):
        self.status_code = status_code
        self.detail = {"validation_error": detail, "code": code}
        
        
class BadRequestException(BaseException):
    
    def __init__(self, detail=None, status_code=BAD_REQUEST_STATUS_CODE, code=BAD_REQUEST):
        self.status_code = status_code
        self.detail = {"error_message": detail, "code": code}
        
        
class UnauthorizedException(BaseException):
    
    def __init__(self, detail=None, status_code=UNAUTHORIZED_STATUS_CODE, code=UNAUTHORIZED_ACCESS):
        self.status_code = status_code
        self.detail = {"error_message": detail, "code": code}