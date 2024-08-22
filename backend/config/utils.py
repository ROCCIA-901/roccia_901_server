from typing import Union

from rest_framework import permissions, serializers
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import exception_handler

from config.exceptions import InvalidFieldException, PermissionFailedException


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
        custom_response_data: dict[str, Union[int, str]] = {
            "status_code": exc.status_code,
            "code": exc.default_code,
            "detail": detail,
        }
        return Response(custom_response_data, status=exc.status_code)


class IsMember(permissions.BasePermission):

    def has_permission(self, request: Request, view) -> bool:
        role: str = "부원"
        if request.user.is_authenticated and request.user.role == role:
            return True
        else:
            raise PermissionFailedException


class IsManager(permissions.BasePermission):

    def has_permission(self, request: Request, view):
        role: str = "운영진"
        if request.user.is_authenticated and request.user.role == role:
            return True
        else:
            raise PermissionFailedException


class WorkoutLevelChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        for key, val in self._choices.items():
            if key == int(obj):
                return val

    def to_internal_value(self, data):
        # To support inserts with the value
        for key, val in self._choices.items():
            if val == data:
                return key
        raise InvalidFieldException("난이도가 정확하지 않습니다.")
