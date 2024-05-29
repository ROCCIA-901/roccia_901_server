from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


MYPAGE_RESPONSE_EXAMPLE = OpenApiExample(
    "마이페이지 조회 성공 예시",
    summary="Mypage Response Example",
    description="마이페이지 조회 성공 시의 응답 예시입니다.",
    value={
        "detail": "마이페이지 조회를 성공했습니다.",
        "data": {
            "profile": {
                "username": "김동욱",
                "generation": "8기",
                "role": "운영진",
                "workout_location": "더클라임 신림",
                "workout_level": "빨간색",
                "profile_number": 8,
                "introduction": "안녕하십니까",
            },
            "total_workout_time": 220,
            "records": [{"workout_level": "파란색", "total_count": 6}],
        },
    },
    response_only=True,
)

USER_PROFILE_RESPONSE_EXAMPLE = OpenApiExample(
    "유저 프로필 조회 성공 예시",
    summary="User Profile Response Example",
    description="유저 프로필 조회 성공 시의 응답 예시입니다.",
    value={
        "detail": "마이페이지 조회를 성공했습니다.",
        "data": {
            "profile": {
                "username": "김동욱",
                "generation": "8기",
                "role": "운영진",
                "workout_location": "더클라임 신림",
                "workout_level": "빨간색",
                "profile_number": 8,
                "introduction": "안녕하십니까",
            }
        },
    },
    response_only=True,
)

USER_NOT_EXIST_FAILURE_EXAMPLE = OpenApiExample(
    "존재하지 않는 사용자 예시",
    summary="User Not Exist",
    description="존재하지 않는 사용자일 때의 응답 예시입니다.",
    value={"status_code": 404, "code": "user_not_exist", "detail": "존재하지 않는 사용자입니다."},
    response_only=True,
)

USER_UPDATE_SUCCESS_EXAMPLE = [
    OpenApiExample(
        "사용자 정보 수정 성공 예시",
        summary="User Update Success",
        description="사용자 정보 수정 성공 시의 응답 예시입니다.",
        value={"detail": "사용자 정보 수정을 성공했습니다."},
        response_only=True,
    )
]

USER_UPDATE_400_FAILURE_EXAMPLE = [
    OpenApiExample(
        "필드 비워둘 수 없음 예시",
        summary="Field Cannot Be Blank",
        description="필드가 비워 둘 수 없을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid", "detail": "xx은 비워 둘 수 없습니다."},
        response_only=True,
    ),
    OpenApiExample(
        "지점 정확하지 않음 예시",
        summary="Invalid Field",
        description="지점이 정확하지 않을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "지점이 정확하지 않습니다."},
        response_only=True,
    ),
    OpenApiExample(
        "프로필 번호 정확하지 않음 예시",
        summary="Invalid Profile Number",
        description="프로필 번호가 정확하지 않을 때의 응답 예시입니다.",
        value={"status_code": 400, "code": "invalid_field", "detail": "프로필 번호가 정확하지 않습니다."},
        response_only=True,
    ),
]

USER_UPDATE_404_FAILURE_EXAMPLE = [
    OpenApiExample(
        "존재하지 않는 사용자 예시",
        summary="User Not Exist",
        description="존재하지 않는 사용자일 때의 응답 예시입니다.",
        value={"status_code": 404, "code": "user_not_exist", "detail": "존재하지 않는 사용자입니다."},
        response_only=True,
    )
]

USER_UPDATE_REQUEST_EXAMPLE = [
    OpenApiExample(
        "사용자 정보 변겅 요청 예시",
        summary="User Update API Request body Example",
        description="사용자 정보 변경 요청 Request body 예시입니다.",
        value={
            "workout_location": "더클라임 양재",
            "workout_level": "파란색",
            "profile_number": "2",
            "introduction": "반갑습니다",
        },
        request_only=True,
    )
]
