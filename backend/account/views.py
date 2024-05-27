import random

from django.core.cache import cache
from django.db import transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from account.models import User
from account.schemas import (
    LOGIN_400_FAILURE_EXAMPLE,
    LOGIN_401_FAILURE_EXAMPLE,
    LOGIN_500_FAILURE_EXAMPLE,
    PASSWORD_UPDATE_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE,
    PASSWORD_UPDATE_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE,
    PASSWORD_UPDATE_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE,
    USER_LOGIN_RESPONSE_EXAMPLE,
    USER_REGISTER_AUTH_CODE_VALIDATION_400_FAILURE_EXAMPLE,
    USER_REGISTER_AUTH_CODE_VALIDATION_RESPONSE_EXAMPLE,
    USER_REGISTER_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE,
    USER_REGISTER_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE,
    USER_REGISTER_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE,
    USER_REGISTRATION_FAILURE_EXAMPLE,
    USER_REGISTRATION_RESPONSE_EXAMPLE,
    ErrorResponseSerializer,
)
from account.serializers import (
    CustomTokenRefreshSerializer,
    LogoutSerializer,
    PasswordUpdateAuthCodeVerificationSerializer,
    PasswordUpdateEmailVerificationSerializer,
    PasswordUpdateSerializer,
    UserLoginSerializer,
    UserRegisterAuthCodeVerificationSerializer,
    UserRegisterEmailVerificationSerializer,
    UserRegistrationSerializer,
)
from account.tasks import send_auth_code_to_email
from config.exceptions import InvalidRefreshToken, TokenIssuanceException


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="회원가입",
        request=UserRegistrationSerializer,
        # fmt: off
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=UserRegistrationSerializer,
                examples=USER_REGISTRATION_RESPONSE_EXAMPLE
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTRATION_FAILURE_EXAMPLE,
            ),
        },
        # fmt: on
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            # fmt: off
            data={
                "detail": "회원가입에 성공했습니다. 관리자에게 승인 문의 바랍니다.",
                "data": {
                    "user": serializer.data,
                }
            },
            status=status.HTTP_201_CREATED
            # fmt: on
        )


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="로그인",
        request=UserLoginSerializer,
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserLoginSerializer,
                examples=USER_LOGIN_RESPONSE_EXAMPLE),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGIN_400_FAILURE_EXAMPLE
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGIN_401_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGIN_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
    )
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

    @extend_schema(
        tags=["사용자 인증"],
        summary="회원가입 인증 번호 요청",
        request=UserRegisterEmailVerificationSerializer,
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserRegisterEmailVerificationSerializer,
                examples=USER_REGISTER_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTER_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTER_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = UserRegisterEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver: str = serializer.validated_data.get("email")
        code: int = random.randint(10000, 99999)

        cache.set(f"{receiver}:register:code", code, timeout=600)
        cache.set(f"{receiver}:register:status", "uncertified", timeout=600)

        send_auth_code_to_email.delay("회원가입", receiver, code)

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

    @extend_schema(
        tags=["사용자 인증"],
        summary="회원가입 인증 번호 확인",
        request=UserRegisterAuthCodeVerificationSerializer,
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserRegisterAuthCodeVerificationSerializer,
                examples=USER_REGISTER_AUTH_CODE_VALIDATION_RESPONSE_EXAMPLE
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTER_AUTH_CODE_VALIDATION_400_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
    )
    def post(self, request: Request) -> Response:
        serializer = UserRegisterAuthCodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver: str = serializer.validated_data.get("email")
        cache.set(f"{receiver}:register:status", "certified", timeout=3600)

        return Response(
            # fmt: off
            data={
                "detail": "회원가입을 위한 인증번호 확인에 성공했습니다. 인증은 1시간 동안 유효합니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )


class PasswordUpdateRequestAuthCodeAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="비밀번호 변경 인증 번호 요청",
        request=PasswordUpdateEmailVerificationSerializer,
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=PasswordUpdateEmailVerificationSerializer,
                examples=PASSWORD_UPDATE_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=PASSWORD_UPDATE_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=PASSWORD_UPDATE_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = PasswordUpdateEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver = serializer.validated_data.get("email")
        code = random.randint(10000, 99999)

        cache.set(f"{receiver}:password:code", code, timeout=600)
        cache.set(f"{receiver}:password:status", "uncertified", timeout=600)

        send_auth_code_to_email.delay("비밀번호 변경", receiver, code)

        return Response(
            # fmt: off
            data={
                "detail": "비밀번호 변경을 위한 인증 번호가 전송됐습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )


class PasswordUpdateAuthCodeValidationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = PasswordUpdateAuthCodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver: str = serializer.validated_data.get("email")
        cache.set(f"{receiver}:password:status", "certified", timeout=600)

        return Response(
            # fmt: off
            data={
                "detail": "비밀번호 변경을 위한 인증번호 확인에 성공했습니다. 인증은 10분 동안 유효합니다.",
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
        serializer = LogoutSerializer(data=request.data)
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
        serializer = PasswordUpdateSerializer(data=request.data)
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
