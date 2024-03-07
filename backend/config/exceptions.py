from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidFieldException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "필드값이 유효하지 않습니다."
    default_code = "invalid_field"


class InvalidFieldStateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "필드 상태가 유효하지 않습니다."
    default_code = "invalid_field_state"


class EmptyFieldException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "필수 필드값이 비어있습니다."
    default_code = "empty_field"


class InvalidRefreshToken(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "유효하지 않은 리프레시 토큰입니다."
    default_code = "invalid_refresh_token"


class InvalidAccountException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "유효하지 않은 계정입니다."
    default_code = "invalid_account"


class PermissionFailedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "이 작업을 수행할 권한이 없습니다."
    default_code = "permission_failed"


class NotExistException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "존재하지 않는 자원입니다."
    default_code = "not_exist"


class InternalServerException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "서버 내부에서 발생한 오류입니다."
    default_code = "internal_server_error"


class TokenIssuanceException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "토큰 발급 중에 문제가 발생했습니다."
    default_code = "token_issuance_error"


class EmailSendingFailedException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "이메일 전송 중에 문제가 발생했습니다."
    default_code = "email_sending_failed"
