from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from config.exceptions import UserNotExistException
from mypage.schemas import (
    MYPAGE_RESPONSE_EXAMPLE,
    USER_NOT_EXIST_FAILURE_EXAMPLE,
    USER_PROFILE_RESPONSE_EXAMPLE,
    USER_UPDATE_400_FAILURE_EXAMPLE,
    USER_UPDATE_404_FAILURE_EXAMPLE,
    USER_UPDATE_SUCCESS_EXAMPLE,
    ErrorResponseSerializer,
)
from mypage.serializers import (
    MypageSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)


class MypageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["마이페이지"],
        summary="마이페이지 조회",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="조회할 유저의 ID",
                required=False,
                type=str,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=MypageSerializer,
                examples=[MYPAGE_RESPONSE_EXAMPLE, USER_PROFILE_RESPONSE_EXAMPLE],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[USER_NOT_EXIST_FAILURE_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        user_id = request.query_params.get("user_id")

        if user_id:
            user = User.objects.filter(id=user_id).first()
            if not user:
                raise UserNotExistException()

            serializer = UserProfileSerializer(user)
        else:
            user = request.user
            serializer = MypageSerializer(user)

        return Response(
            data={
                "detail": "마이페이지 조회를 성공했습니다.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["마이페이지"],
        summary="사용자 정보 수정",
        request=UserUpdateSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserUpdateSerializer,
                examples=USER_UPDATE_SUCCESS_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_UPDATE_400_FAILURE_EXAMPLE,
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_UPDATE_404_FAILURE_EXAMPLE,
            ),
        },
    )
    def patch(self, request: Request) -> Response:
        user = request.user
        if not user:
            raise UserNotExistException()

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "detail": "사용자 정보 수정을 성공했습니다.",
            },
            status=status.HTTP_200_OK,
        )
