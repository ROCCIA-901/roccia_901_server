from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


USER_REGISTRATION_REQUEST_EXAMPLE = [
    OpenApiExample(
        "회원가입 요청 예시",
        summary="User Registration Request body Example",
        description="회원가입 Request body 요청 예시입니다.",
        value={
            "email": "test@gamil.com",
            "password": "Asdf1234!",
            "password_confirmation": "Asdf1234!",
            "username": "홍길동",
            "generation": "8기",
            "role": "운영진",
            "workout_location": "양재",
            "workout_level": "파란색",
            "profile_number": 1,
            "introduction": "안녕하세요",
        },
        request_only=True,
    )
]

USER_REGISTRATION_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "회원가입 응답 예시",
        summary="User Registration Response Example",
        description="회원가입 응답 예시입니다.",
        value={
            "detail": "회원가입에 성공했습니다.",
            "data": {
                "user": {
                    "email": "test@gamil.com",
                    "username": "김동욱",
                    "generation": "8기",
                    "role": "운영진",
                    "workout_location": "양재",
                    "workout_level": "파란색",
                    "profile_number": 1,
                    "introduction": "안녕하세요",
                }
            },
        },
        response_only=True,
    )
]

USER_REGISTRATION_FAILURE_EXAMPLE = [
    OpenApiExample(
        "이메일 중복 예시",
        summary="Duplicate Email",
        description="이미 존재하는 이메일로 요청했을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "이미 존재하는 이메일입니다."},
        response_only=True,
    ),
    OpenApiExample(
        "필수 입력 항목 누락 예시",
        summary="Missing Required Field",
        description="필수 입력 항목을 누락했을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid", "detail": "xx은 필수 입력 항목입니다."},
        response_only=True,
    ),
    OpenApiExample(
        "빈 필드 예시",
        summary="Empty Field",
        description="필수 입력 항목이 빈 문자열일 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid", "detail": "xx은 비워 둘 수 없습니다."},
        response_only=True,
    ),
]


USER_LOGIN_REQUEST_EXAMPLE = [
    OpenApiExample(
        "로그인 요청 예시",
        summary="User Login Request body Example",
        description="로그인 Request body 요청 예시입니다.",
        value={"email": "test@gamil.com", "password": "Asdf1234!"},
        request_only=True,
    )
]

USER_LOGIN_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "로그인 응답 예시",
        summary="User Login Response Example",
        description="로그인 응답 예시입니다.",
        value={
            "detail": "로그인에 성공했습니다.",
            "data": {
                "token": {
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBl...",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXB...",
                }
            },
        },
        response_only=True,
    )
]

LOGIN_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "필수 입력 항목 누락 예시",
        summary="Missing Required Field",
        description="필수 입력 항목을 누락했을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid", "detail": "xx은 필수 입력 항목입니다."},
        response_only=True,
    ),
    OpenApiExample(
        "빈 필드 예시",
        summary="Empty Field",
        description="필수 입력 항목이 빈 문자열일 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid", "detail": "xx은 비워 둘 수 없습니다."},
        response_only=True,
    ),
    OpenApiExample(
        "이메일 또는 비밀번호 유효하지 않음 예시",
        summary="Invalid Email or Password",
        description="이메일 또는 비밀번호가 유효하지 않을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "이메일 또는 비밀번호가 유효하지 않습니다."},
        response_only=True,
    ),
]

LOGIN_401_FAILURE_EXAMPLE = [
    OpenApiExample(
        "유효하지 않은 계정 예시",
        summary="Invalid Account",
        description="유효하지 않은 계정일 때의 응답 예시입니다.",
        value={"status_code": 401, "code": "invalid_account", "detail": "유효하지 않은 계정입니다."},
        response_only=True,
    ),
    OpenApiExample(
        "가입 승인 필요 예시",
        summary="Account Approval Needed",
        description="가입 승인이 필요한 계정일 때의 응답 예시입니다.",
        value={
            "status_code": 401,
            "code": "invalid_account",
            "detail": "가입 승인이 필요한 계정입니다. 관리자에게 문의해주세요.",
        },
        response_only=True,
    ),
]

LOGIN_500_FAILURE_EXAMPLE = [
    OpenApiExample(
        "토큰 발급 오류 예시",
        summary="Token Issuance Error",
        description="토큰 발급 중에 문제가 발생했을 때의 응답 예시입니다.",
        value={"status_code": 500, "code": "token_issuance_error", "detail": "토큰 발급 중에 문제가 발생했습니다."},
        response_only=True,
    )
]
