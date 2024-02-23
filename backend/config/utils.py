from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.authentication import (
    AuthenticationFailed,
    InvalidToken,
    TokenError,
)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        return Response({"message": "인증에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, InvalidToken):
        return Response({"message": "유효하지 않은 토큰입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, TokenError):
        return Response({"message": "토큰 처리 중 오류가 발생했습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    if response is not None and "message" not in response.data:
        error_messages = []

        for field, messages in response.data.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(messages)

        combined_message = " ".join(error_messages)
        response.data = {"message": combined_message}
    return response
