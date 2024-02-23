from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import exception_handler

from config.exceptions import PermissionFailedException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

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
