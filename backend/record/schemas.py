from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


RECORD_CREATE_REQUEST_EXAMPLE = [
    OpenApiExample(
        "운동 기록 생성 요청 예시",
        summary="Record Create Request Example",
        description="운동 기록 생성 요청의 예시입니다.",
        value={
            "location": "더클라임 연남",
            "start_time": "2024-01-02T17:30:00+09:00",
            "end_time": "2024-01-02T19:00:00+09:00",
            "completed_climbs": [{"level": "파랑", "number_of_completions": 3}],
        },
        request_only=True,
    )
]

RECORD_CREATE_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "운동 기록 생성 성공 예시",
        summary="Record Create Response Example",
        description="운동 기록 생성 성공 시의 응답 예시입니다.",
        value={"detail": "운동 기록이 생성되었습니다."},
        response_only=True,
    )
]

RECORD_CREATE_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "운동 종료 후 기록할 수 없음 예시",
        summary="Invalid End Time",
        description="운동 종료 후 기록할 수 없을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "운동 종료 후 기록할 수 있습니다."},
        response_only=True,
    ),
    OpenApiExample(
        "지점 정확하지 않음 예시",
        summary="Invalid Location",
        description="지점이 정확하지 않을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "지점이 정확하지 않습니다."},
        response_only=True,
    ),
    OpenApiExample(
        "기록 존재 예시",
        summary="Record Exists",
        description="해당일에 이미 기록이 존재할 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "해당일에 이미 기록이 존재합니다."},
        response_only=True,
    ),
    OpenApiExample(
        "시간 오류 예시",
        summary="Invalid Time",
        description="시작 시간이 종료 시간보다 같거나 늦을 때의 응답 예시입니다.",
        value={
            "status_code": 400,
            "code": "invalid_field",
            "detail": "시작 시간이 종료 시간보다 같거나 늦을 수 없습니다.",
        },
        response_only=True,
    ),
]

RECORD_CREATE_401_FAILURE_EXAMPLE = [
    OpenApiExample(
        "유효하지 않은 계정 예시",
        summary="Invalid Account",
        description="유효하지 않은 계정일 때의 응답 예시입니다.",
        value={"status_code": 401, "code": "invalid_account", "detail": "유효하지 않은 계정입니다."},
        response_only=True,
    )
]

RECORD_CREATE_403_FAILURE_EXAMPLE = [
    OpenApiExample(
        "권한 없음 예시",
        summary="Permission Denied",
        description="이 작업을 수행할 권한이 없을 때의 응답 예시입니다.",
        value={"status_code": 403, "code": "permission_failed", "detail": "이 작업을 수행할 권한이 없습니다."},
        response_only=True,
    )
]

RECORD_CREATE_500_FAILURE_EXAMPLE = [
    OpenApiExample(
        "서버 내부 오류 예시",
        summary="Internal Server Error",
        description="서버 내부에서 발생한 오류일 때의 응답 예시입니다.",
        value={"status_code": 500, "code": "internal_server_error", "detail": "서버 내부에서 발생한 오류입니다."},
        response_only=True,
    )
]
