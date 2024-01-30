from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidFieldException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"message": "필드값이 유효하지 않습니다."}
    default_code = "invalid_field"


class InternalServerException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = {"message": "서버 내부에서 발생한 오류입니다."}
    default_code = "internal_server_error"

