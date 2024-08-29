from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField()


RANKING_WEEKS_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "주차별 랭킹 목록 조회 성공 예시",
        summary="Weekly Rankings Response Example",
        description="주차별 랭킹 목록 조회 성공 시의 응답 예시입니다.",
        value={
            "detail": "주차별 랭킹 목록 조회를 성공했습니다.",
            "data": {
                "current_generation_week": 5,
                "weekly_rankings": [
                    {
                        "week": 1,
                        "ranking": [
                            {
                                "score": 71.5,
                                "user_id": 28,
                                "username": "조동욱",
                                "user_generation": "5기",
                                "user_workout_location": "더클라임 홍대",
                                "user_workout_level": "파랑색",
                                "user_profile_number": 6,
                            },
                            # ... other user rankings
                        ],
                    },
                    {
                        "week": 2,
                        "ranking": [
                            {
                                "score": 68.3,
                                "user_id": 30,
                                "username": "김철수",
                                "user_generation": "5기",
                                "user_workout_location": "클라이밍 짐 강남",
                                "user_workout_level": "빨강색",
                                "user_profile_number": 10,
                            },
                            # ... other user rankings
                        ],
                    },
                    # ... other weeks
                ],
            },
        },
        response_only=True,
    )
]

RANKING_401_FAILURE_EXAMPLE = [
    OpenApiExample(
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
]

RANKING_500_FAILURE_EXAMPLE = [
    OpenApiExample(
        "서버 내부 오류 예시",
        summary="Internal Server Error",
        description="서버 내부에서 발생한 오류일 때의 응답 예시입니다.",
        value={
            "status_code": 500,
            "code": "internal_server_error",
            "detail": "서버 내부에서 발생한 오류입니다.",
        },
        response_only=True,
    )
]

RANKING_GENERATIONS_RESPONSE_EXAMPLE = [
    OpenApiExample(
        "기수별 랭킹 목록 조회 성공 예시",
        summary="Generations Rankings Response Example",
        description="기수별 랭킹 목록 조회 성공 시의 응답 예시입니다.",
        value={
            "detail": "기수별 랭킹 조회를 성공했습니다.",
            "data": {
                "generation_rankings": [
                    {
                        "generation": "5기",
                        "ranking": [
                            {
                                "score": 71.5,
                                "user_id": 28,
                                "username": "조동욱",
                                "user_generation": "5기",
                                "user_workout_location": "더클라임 홍대",
                                "user_workout_level": "파랑색",
                                "user_profile_number": 6,
                            },
                            # ... other user rankings
                        ],
                    },
                    {
                        "generation": "6기",
                        "ranking": [
                            {
                                "score": 68.3,
                                "user_id": 30,
                                "username": "김철수",
                                "user_generation": "6기",
                                "user_workout_location": "클라이밍 짐 강남",
                                "user_workout_level": "빨강색",
                                "user_profile_number": 10,
                            },
                            # ... other user rankings
                        ],
                    },
                    # ... other generation rankings
                ]
            },
        },
        response_only=True,
    )
]
