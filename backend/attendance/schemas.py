from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


class AttendanceStatusResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = serializers.DictField()


ATTENDANCE_STATUS_SUCCESS_EXAMPLE = OpenApiExample(
    "출석 현황 조회 성공 예시",
    summary="Attendance Status Success",
    description="출석 현황 조회가 성공적으로 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "출석 현황 조회를 성공했습니다.",
        "data": {
            "attendance": ["2024-08-27", "2024-08-28"],
            "late": ["2024-08-26"],
        },
    },
    response_only=True,
)

INVALID_ACCOUNT_EXAMPLE = OpenApiExample(
    "유효하지 않은 계정 예시",
    summary="Invalid Account",
    description="유효하지 않은 계정일 때의 응답 예시입니다.",
    value={
        "status_code": 401,
        "code": "invalid_account",
        "detail": "유효하지 않은 계정입니다.",
    },
    response_only=True,
)

PERMISSION_DENIED_EXAMPLE = OpenApiExample(
    "권한 없음 예시",
    summary="Permission Denied",
    description="이 작업을 수행할 권한이 없을 때의 응답 예시입니다.",
    value={
        "status_code": 403,
        "code": "permission_failed",
        "detail": "이 작업을 수행할 권한이 없습니다.",
    },
    response_only=True,
)

INTERNAL_SERVER_ERROR_EXAMPLE = OpenApiExample(
    "서버 내부 오류 예시",
    summary="Internal Server Error",
    description="서버 내부에서 발생한 오류일 때의 응답 예시입니다.",
    value={"status_code": 500, "code": "internal_server_error", "detail": "서버 내부에서 발생한 오류입니다."},
    response_only=True,
)

ATTENDANCE_REQUEST_SUCCESS_EXAMPLE = OpenApiExample(
    "출석 요청 성공 예시",
    summary="Attendance Request Success",
    description="출석 요청이 성공적으로 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "출석 요청이 정상적으로 처리됐습니다.",
    },
    response_only=True,
)

ATTENDANCE_PERIOD_INVALID_EXAMPLE = OpenApiExample(
    "유효하지 않은 출석 기간 예시",
    summary="Attendance Period Invalid",
    description="유효하지 않은 출석 기간일 때의 응답 예시입니다.",
    value={
        "status_code": 400,
        "code": "attendance_period_invalid",
        "detail": "출석 가능 기간이 아닙니다.",
    },
    response_only=True,
)

DUPLICATE_ATTENDANCE_EXAMPLE = OpenApiExample(
    "중복 출석 요청 예시",
    summary="Duplicate Attendance",
    description="이미 출석 요청이 처리되었거나 대기 중일 때의 응답 예시입니다.",
    value={
        "status_code": 400,
        "code": "duplicate_attendance",
        "detail": "이미 처리된 출석 요청이 있거나 처리 대기 중입니다.",
    },
    response_only=True,
)
