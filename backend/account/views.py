import random

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import AuthStatus, User
from account.serializers import (
    AuthCodeVerificationSerializer,
    EmailVerificationSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)
from config.exceptions import EmailSendingFailedException, TokenIssuanceException


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


class RequestAuthCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver = serializer.validated_data.get("email")
        code = random.randint(10000, 99999)
        try:
            email_subject = "[ROCCIA 901] 본인 확인 인증번호 입니다."
            email_body = f"본인확인을 위해 인증번호 [{code}]를 입력해 주세요."

            send_mail(subject=email_subject, message=email_body, from_email="ROCCIA 901", recipient_list=[receiver])
        except Exception as e:
            raise EmailSendingFailedException()

        AuthStatus.objects.update_or_create(email=receiver, defaults={"code": code})

        return Response(
            # fmt: off
            data={
                "detail": "인증 번호가 전송됐습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )


class AuthCodeValidationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = AuthCodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        AuthStatus.objects.filter(email=email).update(status=True)
        return Response(
            # fmt: off
            data={
                "detail": "인증번호 확인에 성공했습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )
