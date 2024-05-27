# schemas.py
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
                "introduction": "안녕하십니",
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
