from typing import Union

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context) -> Response:
    response = exception_handler(exc, context)

    if isinstance(exc, APIException):
        message: str = ""
        if response is not None:
            if "detail" not in response.data:
                error_messages: list = []
                for messages in response.data.values():
                    if isinstance(messages, str):
                        error_messages.append(messages)
                    elif isinstance(messages, list):
                        error_messages.extend(messages)
                    else:
                        error_messages.append(str(messages))
                message = " ".join(error_messages)
            else:
                message = response.data.get("detail")

        detail: str = exc.detail if not message else message
        # fmt: off
        custom_response_data: dict[str, Union[int, str]] = {
            "status_code": exc.status_code,
            "code": exc.default_code,
            "detail": detail
        }
        # fmt: on
        return Response(custom_response_data, status=exc.status_code)
