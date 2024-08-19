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
    CUSTOM_TOKEN_REFRESH_400_FAILURE_EXAMPLE,
    CUSTOM_TOKEN_REFRESH_RESPONSE_EXAMPLE,
    LOGIN_400_FAILURE_EXAMPLE,
    LOGIN_401_FAILURE_EXAMPLE,
    LOGIN_500_FAILURE_EXAMPLE,
    LOGOUT_400_FAILURE_EXAMPLE,
    LOGOUT_401_FAILURE_EXAMPLE,
    LOGOUT_RESPONSE_EXAMPLE,
    PASSWORD_UPDATE_400_FAILURE_EXAMPLE,
    PASSWORD_UPDATE_AUTH_CODE_VALIDATION_400_FAILURE_EXAMPLE,
    PASSWORD_UPDATE_AUTH_CODE_VALIDATION_RESPONSE_EXAMPLE,
    PASSWORD_UPDATE_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE,
    PASSWORD_UPDATE_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE,
    PASSWORD_UPDATE_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE,
    PASSWORD_UPDATE_RESPONSE_EXAMPLE,
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
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=UserRegistrationSerializer,
                examples=USER_REGISTRATION_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTRATION_FAILURE_EXAMPLE,
            ),
        },
    )
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "detail": "회원가입에 성공했습니다. 관리자에게 승인 문의 바랍니다.",
                "data": {
                    "user": serializer.data,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="로그인",
        request=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserLoginSerializer,
                examples=USER_LOGIN_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGIN_400_FAILURE_EXAMPLE,
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGIN_401_FAILURE_EXAMPLE,
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGIN_500_FAILURE_EXAMPLE,
            ),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user: User = serializer.validated_data["user"]
            token = TokenObtainPairSerializer.get_token(user)
            token["role"] = user.role
            access_token: str = str(token.access_token)
            refresh_token: str = str(token)
        except TokenError:
            raise TokenIssuanceException("토큰 발급 중에 문제가 발생했습니다.")

        return Response(
            data={
                "detail": "로그인에 성공했습니다.",
                "data": {
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
            },
            status=status.HTTP_200_OK,
        )


class UserRegisterRequestAuthCodeAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="회원가입 인증 번호 요청",
        request=UserRegisterEmailVerificationSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserRegisterEmailVerificationSerializer,
                examples=USER_REGISTER_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTER_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE,
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTER_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE,
            ),
        },
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
            data={
                "detail": "회원가입을 위한 인증번호가 전송됐습니다.",
            },
            status=status.HTTP_200_OK,
        )


class UserRegisterAuthCodeValidationAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="회원가입 인증 번호 확인",
        request=UserRegisterAuthCodeVerificationSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserRegisterAuthCodeVerificationSerializer,
                examples=USER_REGISTER_AUTH_CODE_VALIDATION_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=USER_REGISTER_AUTH_CODE_VALIDATION_400_FAILURE_EXAMPLE,
            ),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = UserRegisterAuthCodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver: str = serializer.validated_data.get("email")
        cache.set(f"{receiver}:register:status", "certified", timeout=3600)

        return Response(
            data={
                "detail": "회원가입을 위한 인증번호 확인에 성공했습니다. 인증은 1시간 동안 유효합니다.",
            },
            status=status.HTTP_200_OK,
        )


class PasswordUpdateRequestAuthCodeAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="비밀번호 변경 인증 번호 요청",
        request=PasswordUpdateEmailVerificationSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=PasswordUpdateEmailVerificationSerializer,
                examples=PASSWORD_UPDATE_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=PASSWORD_UPDATE_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE,
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=PASSWORD_UPDATE_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE,
            ),
        },
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
            data={
                "detail": "비밀번호 변경을 위한 인증 번호가 전송됐습니다.",
            },
            status=status.HTTP_200_OK,
        )


class PasswordUpdateAuthCodeValidationAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="비밀번호 변경 인증 번호 확인",
        request=PasswordUpdateAuthCodeVerificationSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=PasswordUpdateAuthCodeVerificationSerializer,
                examples=PASSWORD_UPDATE_AUTH_CODE_VALIDATION_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=PASSWORD_UPDATE_AUTH_CODE_VALIDATION_400_FAILURE_EXAMPLE,
            ),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = PasswordUpdateAuthCodeVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver: str = serializer.validated_data.get("email")
        cache.set(f"{receiver}:password:status", "certified", timeout=600)

        return Response(
            data={
                "detail": "비밀번호 변경을 위한 인증번호 확인에 성공했습니다. 인증은 10분 동안 유효합니다.",
            },
            status=status.HTTP_200_OK,
        )


class CustomTokenRefreshAPIView(TokenRefreshView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="토큰 재발급",
        request=CustomTokenRefreshSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=CustomTokenRefreshSerializer,
                examples=CUSTOM_TOKEN_REFRESH_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=CUSTOM_TOKEN_REFRESH_400_FAILURE_EXAMPLE,
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "detail": "액세스 토큰 발급을 성공했습니다.",
                "data": {
                    "token": {
                        "access": serializer.validated_data["access"],
                    },
                },
            },
        )


class UserLogoutAPIView(APIView):

    @extend_schema(
        tags=["사용자 인증"],
        summary="로그아웃",
        request=LogoutSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=LogoutSerializer,
                examples=LOGOUT_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGOUT_400_FAILURE_EXAMPLE,
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=LOGOUT_401_FAILURE_EXAMPLE,
            ),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token: RefreshToken = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
        except Exception as e:
            raise InvalidRefreshToken()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "detail": "로그아웃에 성공했습니다.",
            },
        )


class UserPasswordUpdateAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["사용자 인증"],
        summary="비밀번호 변경",
        request=PasswordUpdateSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=PasswordUpdateSerializer,
                examples=PASSWORD_UPDATE_RESPONSE_EXAMPLE,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=PASSWORD_UPDATE_400_FAILURE_EXAMPLE,
            ),
        },
    )
    def patch(self, request: Request) -> Response:
        serializer = PasswordUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_200_OK,
            data={
                "detail": "비밀번호 변경에 성공했습니다.",
            },
        )
