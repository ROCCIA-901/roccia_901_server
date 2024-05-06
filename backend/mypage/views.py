from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from config.exceptions import UserNotExistException
from mypage.serializers import (
    MypageSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)


def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except Exception:
        raise UserNotExistException()


class MypageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        user_id = request.query_params.get("user_id")

        if user_id:
            user = get_user(user_id)
            serializer = UserProfileSerializer(user)
        else:
            user = request.user
            if not user:
                raise UserNotExistException()

            serializer = MypageSerializer(user)

        return Response(
            # fmt: off
            data={
                "detail": "마이페이지 조회를 성공했습니다.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
            # fmt: on
        )

    def patch(self, request: Request) -> Response:
        user = request.user
        if not user:
            raise UserNotExistException()

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            # fmt: off
            data={
                "detail": "사용자 정보 수정을 성공했습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )
