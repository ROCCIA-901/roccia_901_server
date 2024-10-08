from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers

from attendance.serializers import AttendanceRequestListSerializer, UserListSerializer


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


class AttendanceStatusResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = serializers.DictField()


class AttendanceRequestListResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = AttendanceRequestListSerializer(many=True)


class ApprovalResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class RejectionResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class AttendanceRateResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = serializers.DictField(child=serializers.FloatField())


class AttendanceRecordResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = serializers.DictField()


class WorkoutLocationResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = serializers.DictField()


class UserListResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = UserListSerializer(many=True)


USER_LIST_SUCCESS_EXAMPLE = OpenApiExample(
    "부원 목록 조회 성공 예시",
    summary="User List Success",
    description="현재 활성화된 부원들의 목록 조회가 성공적으로 처리되었을 때의 응답 예시입니다. 각 부원의 출석률과 운동 수준이 포함됩니다.",
    value={
        "detail": "부원 목록 조회를 성공했습니다.",
        "data": [
            {
                "id": 1,
                "username": "member1",
                "profile_number": "1",
                "workout_location": "더클라임 신림",
                "workout_level": "빨간색",
                "generation": "11기",
                "attendance_rate": 85.75,
            },
            {
                "id": 2,
                "username": "member2",
                "profile_number": "1",
                "workout_location": "더클라임 신림",
                "workout_level": "파란색",
                "generation": "11기",
                "attendance_rate": 90.25,
            },
        ],
    },
    response_only=True,
)


WORKOUT_LOCATION_SUCCESS_EXAMPLE = OpenApiExample(
    "금일 운동 지점 조회 성공 예시",
    summary="Workout Location Success",
    description="현재 날짜의 운동 지점 조회가 성공적으로 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "금일 운동 지점 조회를 성공했습니다.",
        "data": {
            "workout_location": "더클라임 신림",
        },
    },
    response_only=True,
)


ATTENDANCE_RECORD_SUCCESS_EXAMPLE = OpenApiExample(
    "출석 내역 조회 성공 예시",
    summary="Attendance Record Success",
    description="특정 사용자의 출석 내역 조회가 성공적으로 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "출석 내역 조회를 성공했습니다.",
        "data": {
            "count": {
                "attendance": 10,
                "late": 2,
                "absence": 1,
                "alternative": 1,
            },
            "detail": [
                {
                    "week": 1,
                    "status": "출석",
                    "date": "2024-08-05",
                },
                {
                    "week": 2,
                    "status": "지각",
                    "date": "2024-08-12",
                },
            ],
        },
    },
    response_only=True,
)


ATTENDANCE_RATE_SUCCESS_EXAMPLE = OpenApiExample(
    "사용자 출석률 조회 성공 예시",
    summary="Attendance Rate Success",
    description="사용자의 출석률 조회가 성공적으로 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "사용자 출석률 조회를 성공했습니다.",
        "data": {
            "attendance_rate": 85.75,
        },
    },
    response_only=True,
)


REJECTION_SUCCESS_EXAMPLE = OpenApiExample(
    "출석 요청 거절 성공 예시",
    summary="Rejection Success",
    description="출석 요청이 성공적으로 거절 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "요청 거절이 성공적으로 완료되었습니다.",
    },
    response_only=True,
)


APPROVAL_SUCCESS_EXAMPLE = OpenApiExample(
    "출석 요청 승인 성공 예시",
    summary="Approval Success",
    description="출석 요청이 성공적으로 승인 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "요청 승인이 성공적으로 완료되었습니다.",
    },
    response_only=True,
)

INVALID_FIELD_STATE_EXAMPLE = OpenApiExample(
    "유효하지 않은 필드 상태 예시",
    summary="Invalid Field State",
    description="이미 처리된 요청이거나 유효하지 않은 필드 상태일 때의 응답 예시입니다.",
    value={
        "status_code": 400,
        "code": "invalid_field_state",
        "detail": "필드 상태가 유효하지 않습니다.",
    },
    response_only=True,
)

NOT_EXIST_EXAMPLE = OpenApiExample(
    "존재하지 않는 자원 예시",
    summary="Not Exist",
    description="존재하지 않는 자원에 접근하려 할 때의 응답 예시입니다.",
    value={
        "status_code": 404,
        "code": "not_exist",
        "detail": "존재하지 않는 자원입니다.",
    },
    response_only=True,
)

RESOURCE_LOCKED_EXAMPLE = OpenApiExample(
    "자원 잠김 예시",
    summary="Resource Locked",
    description="해당 자원이 잠겨 있어 작업을 수행할 수 없을 때의 응답 예시입니다.",
    value={
        "status_code": 423,
        "code": "resource_locked",
        "detail": "해당 자원이 잠겨 있어 작업을 수행할 수 없습니다.",
    },
    response_only=True,
)


ATTENDANCE_REQUEST_LIST_SUCCESS_EXAMPLE = OpenApiExample(
    "출석 요청 목록 조회 성공 예시",
    summary="Attendance Request List Success",
    description="출석 요청 목록 조회가 성공적으로 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "출석 요청 목록 조회를 성공했습니다.",
        "data": [
            {
                "user": "username1",
                "generation": "11기",
                "request_time": "2024-08-28T14:30:00Z",
                "workout_location": "더클라임 신림",
                "week": 5,
            },
            {
                "user": "username2",
                "generation": "11기",
                "request_time": "2024-08-27T10:00:00Z",
                "workout_location": "더클라임 신림",
                "week": 5,
            },
        ],
    },
    response_only=True,
)

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

LATEST_GENERATION_SUCCESS_EXAMPLE = OpenApiExample(
    "최근 기수 조회 성공 예시",
    summary="Latest Generation Success",
    description="최근 기수 조회가 성공적으로 처리되었을 때의 응답 예시입니다.",
    value={
        "detail": "최근 기수 조회를 성공했습니다.",
        "data": {
            "generation": 12,
        },
    },
    response_only=True,
)
