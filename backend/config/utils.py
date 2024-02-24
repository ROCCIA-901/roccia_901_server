from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.authentication import (
    AuthenticationFailed,
    InvalidToken,
    TokenError,
)

from config.exceptions import (
    AuthenticationFailedException,
    InvalidTokenException,
    TokenErrorException,
)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        raise AuthenticationFailedException()
    elif isinstance(exc, InvalidToken):
        raise InvalidTokenException()
    elif isinstance(exc, TokenError):
        raise TokenErrorException()

    if isinstance(exc, APIException):
        combined_message = ""
        if response is not None and "detail" not in response.data:
            error_messages = []
            for messages in response.data.values():
                if isinstance(messages, str):
                    error_messages.append(messages)
                elif isinstance(messages, list):
                    error_messages.extend(messages)
                else:
                    error_messages.append(str(messages))
            combined_message = " ".join(error_messages)

        detail = exc.detail if not combined_message else combined_message
        custom_response_data = {"status_code": exc.status_code, "code": exc.default_code, "detail": detail}
        return Response(custom_response_data, status=exc.status_code)
