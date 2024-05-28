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

RECORD_401_FAILURE_EXAMPLE = [
    OpenApiExample(
        "유효하지 않은 계정 예시",
        summary="Invalid Account",
        description="유효하지 않은 계정일 때의 응답 예시입니다.",
        value={"status_code": 401, "code": "invalid_account", "detail": "유효하지 않은 계정입니다."},
        response_only=True,
    )
]

RECORD_403_FAILURE_EXAMPLE = [
    OpenApiExample(
        "권한 없음 예시",
        summary="Permission Denied",
        description="이 작업을 수행할 권한이 없을 때의 응답 예시입니다.",
        value={"status_code": 403, "code": "permission_failed", "detail": "이 작업을 수행할 권한이 없습니다."},
        response_only=True,
    )
]

RECORD_500_FAILURE_EXAMPLE = [
    OpenApiExample(
        "서버 내부 오류 예시",
        summary="Internal Server Error",
        description="서버 내부에서 발생한 오류일 때의 응답 예시입니다.",
        value={"status_code": 500, "code": "internal_server_error", "detail": "서버 내부에서 발생한 오류입니다."},
        response_only=True,
    )
]

RECORD_UPDATE_REQUEST_EXAMPLE = [
    OpenApiExample(
        "운동 기록 수정 요청 예시",
        summary="Record Update Request Example",
        description="운동 기록 수정 요청의 예시입니다.",
        value={
            "workout_location": "더클라임 연남",
            "start_time": "2024-01-02T17:30:00+09:00",
            "end_time": "2024-01-02T19:00:00+09:00",
            "boulder_problems": [{"workout_level": "파랑", "count": 3}],
        },
        request_only=True,
    )
]

RECORD_UPDATE_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "운동 기록 수정 성공 예시",
        summary="Record Update Response Example",
        description="운동 기록 수정 성공 시의 응답 예시입니다.",
        value={"detail": "운동 기록이 수정되었습니다."},
        response_only=True,
    )
]

RECORD_LIST_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "운동 기록 전체 조회 성공 예시",
        summary="Record List Response Example",
        description="운동 기록 전체 조회 성공 시의 응답 예시입니다.",
        value={
            "message": "모든 운동 기록을 가져왔습니다.",
            "data": {
                "records": [
                    {
                        "climbing_record_id": 1,
                        "user_id": 12345,
                        "location": "더클라임 홍대",
                        "start_time": "2024-01-04T17:30:00+09:00",
                        "end_time": "2024-01-04T19:00:00+09:00",
                        "boulder_problem_set": [
                            {"level": "초록", "number_of_completions": 3},
                            {"level": "파랑", "number_of_completions": 0},
                        ],
                    },
                    {
                        "climbing_record_id": 2,
                        "user_id": 12345,
                        "location": "더클라임 양재",
                        "start_time": "2024-01-14T14:30:00+09:00",
                        "end_time": "2024-01-14T16:00:00+09:00",
                        "boulder_problem_set": [
                            {"level": "초록", "number_of_completions": 2},
                            {"level": "파랑", "number_of_completions": 1},
                        ],
                    },
                    {
                        "climbing_record_id": 3,
                        "user_id": 12345,
                        "location": "더클라임 연남",
                        "start_time": "2024-01-20T12:30:00+09:00",
                        "end_time": "2024-01-20T19:00:00+09:00",
                        "boulder_problem_set": [
                            {"level": "초록", "number_of_completions": 4},
                            {"level": "파랑", "number_of_completions": 4},
                        ],
                    },
                ]
            },
        },
        response_only=True,
    )
]

RECORD_DESTROY_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "운동 기록 삭제 성공 예시",
        summary="Record Destroy Response Example",
        description="운동 기록 삭제 성공 시의 응답 예시입니다.",
        value={"detail": "운동 기록이 삭제되었습니다."},
        response_only=True,
    )
]

RECORD_DATES_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "운동 기록 날짜 조회 성공 예시",
        summary="Record Dates Response Example",
        description="운동 기록 날짜 조회 성공 시의 응답 예시입니다.",
        value={
            "detail": "운동 기록 날짜 목록 조회를 성공했습니다.",
            "data": {"dates": ["2024-01-04", "2024-01-14", "2024-01-20"]},
        },
        response_only=True,
    )
]
