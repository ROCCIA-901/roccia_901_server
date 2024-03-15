import random

from django.core.mail import send_mail
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from account.models import (
    PasswordUpdateEmailAuthStatus,
    User,
    UserRegistrationEmailAuthStatus,
)
from account.serializers import (
    CustomTokenRefreshSerializer,
    LogoutSerializer,
    PasswordUpdateEmailVerificationSerializer,
    PasswordUpdateSerializer,
    UserLoginSerializer,
    UserRegisterAuthCodeVerificationSerializer,
    UserRegisterEmailVerificationSerializer,
    UserRegistrationSerializer,
)
from config.exceptions import (
    EmailSendingFailedException,
    InvalidRefreshToken,
    TokenIssuanceException,
)


def send_auth_code_to_email(receiver: str, code: int) -> None:
    try:
        email_subject = "[ROCCIA 901] 본인 확인 인증번호 입니다."
        email_body = f"본인확인을 위해 인증번호 [{code}]를 입력해 주세요."

        send_mail(subject=email_subject, message=email_body, from_email="ROCCIA 901", recipient_list=[receiver])
    except Exception as e:
        raise EmailSendingFailedException()


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
            raise TokenIssuanceException("토큰 발급 중에 문제가 발생했습니다.")

        return Response(
            # fmt: off
            data={
                "detail": "회원가입에 성공했습니다.",
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
            raise TokenIssuanceException("토큰 발급 중에 문제가 발생했습니다.")

        return Response(
            # fmt: off
            data={
                "detail": "로그인에 성공했습니다.",
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


class UserRegisterRequestAuthCodeAPIView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = UserRegisterEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver = serializer.validated_data.get("email")
        code = random.randint(10000, 99999)
        send_auth_code_to_email(receiver, code)

        UserRegistrationEmailAuthStatus.objects.update_or_create(email=receiver, defaults={"code": code})

        return Response(
            # fmt: off
            data={
                "detail": "회원가입을 위한 인증번호가 전송됐습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )


class UserRegisterAuthCodeValidationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = UserRegisterAuthCodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        UserRegistrationEmailAuthStatus.objects.filter(email=email).update(status=True)
        return Response(
            # fmt: off
            data={
                "detail": "인증번호 확인에 성공했습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )


class PasswordUpdateRequestAuthCodeAPIView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = PasswordUpdateEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver = serializer.validated_data.get("email")
        code = random.randint(10000, 99999)
        send_auth_code_to_email(receiver, code)

        PasswordUpdateEmailAuthStatus.objects.update_or_create(email=receiver, defaults={"code": code})

        return Response(
            # fmt: off
            data={
                "detail": "비밀번호 변경을 위한 인증 번호가 전송됐습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )


class CustomTokenRefreshAPIView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            # fmt: off
            status=status.HTTP_200_OK,
            data={
                "detail": "액세스 토큰 발급을 성공했습니다.",
                "data": {
                    "token": {
                        "access": serializer.validated_data["access"]
                    }
                },
            },
            # fmt: on
        )


class UserLogoutAPIView(APIView):

    def post(self, request: Request) -> Response:
        serializer: LogoutSerializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token: RefreshToken = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
        except Exception as e:
            raise InvalidRefreshToken()

        return Response(
            # fmt: off
            status=status.HTTP_200_OK,
            data={
                "detail": "로그아웃에 성공했습니다.",
            },
            # fmt: on
        )


class UserPasswordUpdateAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request: Request) -> Response:
        serializer: PasswordUpdateSerializer = PasswordUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            # fmt: off
            status=status.HTTP_200_OK,
            data={
                "detail": "비밀번호 변경에 성공했습니다.",
            },
            # fmt: on
        )
