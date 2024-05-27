from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


USER_REGISTRATION_REQUEST_EXAMPLE = [
    OpenApiExample(
        "회원가입 요청 예시",
        summary="User Registration API Request body Example",
        description="회원가입 Request body 예시입니다.",
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
        summary="User Login API Request body Example",
        description="로그인 Request body 예시입니다.",
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

USER_REGISTER_REQUEST_AUTH_CODE_REQUEST_EXAMPLE = [
    OpenApiExample(
        "회원가입 인증 번호 요청 예시",
        summary="User Register Request Auth Code API Request body Example",
        description="회원가입 인증 번호 요청 Request body 예시입니다.",
        value={"email": "test@naver.com"},
        request_only=True,
    )
]

USER_REGISTER_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "회원가입 인증 번호 응답 예시",
        summary="User Register Request Auth Code API Response body Example",
        description="회원가입 인증 번호 응답 예시입니다.",
        value={"detail": "회원가입을 위한 인증 번호가 전송됐습니다."},
        response_only=True,
    )
]

USER_REGISTER_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "이미 인증 완료된 사용자 예시",
        summary="Already Verified User",
        description="이미 인증 완료된 사용자일 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field_state", "detail": "이미 인증 완료된 사용자입니다."},
        response_only=True,
    )
]

USER_REGISTER_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE = [
    OpenApiExample(
        "이메일 전송 실패 예시",
        summary="Email Sending Failed",
        description="이메일 전송 중에 문제가 발생했을 때의 응답 예시입니다.",
        value={"status_code": 500, "code": "email_sending_failed", "detail": "이메일 전송 중에 문제가 발생했습니다."},
        response_only=True,
    )
]

USER_REGISTER_AUTH_CODE_VALIDATION_REQUEST_EXAMPLE = [
    OpenApiExample(
        "회원가입 인증 번호 확인 요청 예시",
        summary="User Register Auth Code Validation API Request body Example",
        description="회원가입 인증 번호 확인 요청 Request body 예시입니다.",
        value={"email": "test@naver.com", "code": "121099"},
        request_only=True,
    )
]

USER_REGISTER_AUTH_CODE_VALIDATION_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "회원가입 인증 번호 확인 응답 예시",
        summary="User Register Auth Code Validation API Response body Example",
        description="회원가입 인증 번호 확인 응답 예시입니다.",
        value={"detail": "인증번호 확인에 성공했습니다."},
        response_only=True,
    )
]

USER_REGISTER_AUTH_CODE_VALIDATION_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "인증번호 요청 내역 없음 예시",
        summary="No Verification Request",
        description="해당 이메일의 인증번호 요청 내역이 존재하지 않을 때의 응답 예시입니다.",
        value={
            "status_code": 400,
            "code": "invalid_field",
            "detail": "해당 이메일의 인증번호 요청 내역이 존재하지 않습니다.",
        },
        response_only=True,
    ),
    OpenApiExample(
        "이미 인증 완료된 사용자 예시",
        summary="Already Verified User",
        description="이미 인증 완료된 사용자일 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field_state", "detail": "이미 인증 완료된 사용자입니다."},
        response_only=True,
    ),
    OpenApiExample(
        "인증번호 불일치 예시",
        summary="Incorrect Verification Code",
        description="인증번호가 일치하지 않을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "인증번호가 일치하지 않습니다."},
        response_only=True,
    ),
    OpenApiExample(
        "인증번호 유효시간 초과 예시",
        summary="Verification Code Expired",
        description="인증번호의 유효시간이 지났을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "인증번호의 유효시간이 지났습니다."},
        response_only=True,
    ),
]

PASSWORD_UPDATE_REQUEST_AUTH_CODE_REQUEST_EXAMPLE = [
    OpenApiExample(
        "비밀번호 변경 인증 번호 요청 예시",
        summary="Password Update Request Auth Code API Request body Example",
        description="비밀번호 변경 인증 번호 요청 Request body 예시입니다.",
        value={"email": "test@naver.com"},
        request_only=True,
    )
]

PASSWORD_UPDATE_REQUEST_AUTH_CODE_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "비밀번호 변경 인증 번호 응답 예시",
        summary="Password Update Request Auth Code API Response body Example",
        description="비밀번호 변경 인증 번호 응답 예시입니다.",
        value={"detail": "비밀번호 변경을 위한 인증 번호가 전송됐습니다."},
        response_only=True,
    )
]

PASSWORD_UPDATE_REQUEST_AUTH_CODE_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "존재하지 않는 이메일 예시",
        summary="Non-existent Email",
        description="존재하지 않는 이메일일 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "존재하지 않는 이메일입니다."},
        response_only=True,
    )
]

PASSWORD_UPDATE_REQUEST_AUTH_CODE_500_FAILURE_EXAMPLE = [
    OpenApiExample(
        "이메일 전송 실패 예시",
        summary="Email Sending Failed",
        description="이메일 전송 중에 문제가 발생했을 때의 응답 예시입니다.",
        value={"status_code": 500, "code": "email_sending_failed", "detail": "이메일 전송 중에 문제가 발생했습니다."},
        response_only=True,
    )
]

PASSWORD_UPDATE_AUTH_CODE_VALIDATION_REQUEST_EXAMPLE = [
    OpenApiExample(
        "비밀번호 변경 인증 번호 확인 요청 예시",
        summary="Password Update Auth Code Validation API Request body Example",
        description="비밀번호 변경 인증 번호 확인 요청 Request body 예시입니다.",
        value={"email": "test@naver.com", "code": "190056"},
        request_only=True,
    )
]

PASSWORD_UPDATE_AUTH_CODE_VALIDATION_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "비밀번호 변경 인증 번호 확인 응답 예시",
        summary="Password Update Auth Code Validation API Response body Example",
        description="비밀번호 변경 인증 번호 확인 응답 예시입니다.",
        value={"detail": "인증번호 확인에 성공했습니다."},
        response_only=True,
    )
]

PASSWORD_UPDATE_AUTH_CODE_VALIDATION_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "인증번호 요청 내역 없음 예시",
        summary="No Verification Request",
        description="해당 이메일의 인증번호 요청 내역이 존재하지 않을 때의 응답 예시입니다.",
        value={
            "status_code": 400,
            "code": "invalid_field",
            "detail": "해당 이메일의 인증번호 요청 내역이 존재하지 않습니다.",
        },
        response_only=True,
    ),
    OpenApiExample(
        "이미 인증 완료된 사용자 예시",
        summary="Already Verified User",
        description="이미 인증 완료된 사용자일 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field_state", "detail": "이미 인증 완료된 사용자입니다."},
        response_only=True,
    ),
    OpenApiExample(
        "인증번호 불일치 예시",
        summary="Incorrect Verification Code",
        description="인증번호가 일치하지 않을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "인증번호가 일치하지 않습니다."},
        response_only=True,
    ),
    OpenApiExample(
        "인증번호 유효시간 초과 예시",
        summary="Verification Code Expired",
        description="인증번호의 유효시간이 지났을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "인증번호의 유효시간이 지났습니다."},
        response_only=True,
    ),
]

CUSTOM_TOKEN_REFRESH_REQUEST_EXAMPLE = [
    OpenApiExample(
        "토큰 재발급 요청 예시",
        summary="Custom Token Refresh API Request body Example",
        description="토큰 재발급 요청 Request body 예시입니다.",
        value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXB..."},
        request_only=True,
    )
]

CUSTOM_TOKEN_REFRESH_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "토큰 재발급 응답 예시",
        summary="Custom Token Refresh API Response body Example",
        description="토큰 재발급 응답 예시입니다.",
        value={
            "detail": "액세스 토큰 발급을 성공했습니다.",
            "data": {"token": {"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXB..."}},
        },
        response_only=True,
    )
]

CUSTOM_TOKEN_REFRESH_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "필수 필드 누락 예시",
        summary="Missing Required Field",
        description="refresh 필드가 누락되었을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid", "detail": "refresh 필드는 필수 항목입니다."},
        response_only=True,
    ),
    OpenApiExample(
        "유효하지 않은 토큰 예시",
        summary="Invalid Token",
        description="토큰이 유효하지 않을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid", "detail": "토큰이 유효하지 않습니다."},
        response_only=True,
    ),
]
