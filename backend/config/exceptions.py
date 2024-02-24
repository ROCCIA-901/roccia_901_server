from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidFieldException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "필드값이 유효하지 않습니다."
    default_code = "invalid_field"


class EmptyFieldException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "필수 필드값이 비어있습니다."
    default_code = "empty_field"


class InvalidAccountException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "유효하지 않은 계정입니다."
    default_code = "invalid_account"


class AuthenticationFailedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "인증에 실패했습니다."
    default_code = "authentication_failed"


class InvalidTokenException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "유효하지 않은 토큰입니다."
    default_code = "invalid_token"


class TokenErrorException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "토큰 처리 중 오류가 발생했습니다."
    default_code = "token_error"


class InternalServerException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "서버 내부에서 발생한 오류입니다."
    default_code = "internal_server_error"


class TokenIssuanceException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "토큰 발급 중에 문제가 발생했습니다."
    default_code = "token_issuance_error"
