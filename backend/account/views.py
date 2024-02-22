from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import User
from account.serializers import UserLoginSerializer, UserRegistrationSerializer
from config.exceptions import TokenIssuanceException


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()

        try:
            token = TokenObtainPairSerializer.get_token(user)
            access_token: str = str(token.access_token)
            refresh_token: str = str(token)
        except TokenError:
            raise TokenIssuanceException({"message": "토큰 발급 중에 문제가 발생했습니다."})

        return Response(
            # fmt: off
            data={
                "message": "회원가입에 성공했습니다.",
                "data": {
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            },
            status=status.HTTP_201_CREATED
            # fmt: on
        )


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user: User = serializer.validated_data["user"]
            token = TokenObtainPairSerializer.get_token(user)
            access_token: str = str(token.access_token)
            refresh_token: str = str(token)
        except TokenError:
            raise TokenIssuanceException({"message": "토큰 발급 중에 문제가 발생했습니다."})

        return Response(
            # fmt: off
            data={
                "message": "로그인에 성공했습니다.",
                "data": {
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            },
            status=status.HTTP_200_OK
            # fmt: on
        )
