from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


USER_REGISTRATION_REQUEST_EXAMPLE = OpenApiExample(
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

USER_REGISTRATION_RESPONSE_EXAMPLE = OpenApiExample(
    "회원가입 응답 예시",
    summary="User Registration Response Example",
    description="회원가입 응답 예시입니다.",
    value={
        "message": "회원가입에 성공했습니다.",
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

USER_REGISTRATION_FAILURE_EXAMPLES = [
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
