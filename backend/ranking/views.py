from typing import Dict, List

from django.db import models
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from ranking.models import Ranking
from ranking.schemas import (
    RANKING_401_FAILURE_EXAMPLE,
    RANKING_500_FAILURE_EXAMPLE,
    RANKING_GENERATIONS_RESPONSE_EXAMPLE,
    RANKING_WEEKS_RESPONSE_EXAMPLE,
    ErrorResponseSerializer,
)
from ranking.serializers import RankingSerializer


@extend_schema(
    tags=["랭킹"],
    summary="주차별 랭킹 조회",
    # fmt: off
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=RankingSerializer,
            examples=RANKING_WEEKS_RESPONSE_EXAMPLE
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_401_FAILURE_EXAMPLE
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_500_FAILURE_EXAMPLE
        ),
    },
    # fmt: on
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_weekly_rankings(request: Request) -> Response:
    weeks: List[int] = list(set(Ranking.objects.values_list("week", flat=True)))
    weeks.sort()
    data: List[Dict] = []
    for week in weeks:
        weekly_ranking = {
            "week": week,
            "ranking": RankingSerializer(
                Ranking.objects.filter(week=week)
                .values(
                    "week",
                    "user__id",
                    "user__username",
                    "user__generation",
                    "user__workout_location",
                    "user__workout_level",
                    "user__profile_number",
                    "score",
                )
                .order_by("-score"),
                many=True,
            ).data,
        }
        data.append(weekly_ranking)
    return Response(
        data={
            "detail": "주차별 랭킹 목록 조회를 성공했습니다.",
            "data": {
                "weekly_rankings": data,
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["랭킹"],
    summary="기수별 랭킹 조회",
    # fmt: off
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=RankingSerializer,
            examples=RANKING_GENERATIONS_RESPONSE_EXAMPLE
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_401_FAILURE_EXAMPLE
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_500_FAILURE_EXAMPLE
        ),
    },
    # fmt: on
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_generation_rankings(request: Request) -> Response:
    generation_rankings = (
        Ranking.objects.select_related("user")
        .values(
            "generation",
            "user__id",
            "user__username",
            "user__generation",
            "user__workout_location",
            "user__workout_level",
            "user__profile_number",
        )
        .annotate(score=models.Sum("score"))
        .order_by("-score")
    )

    generations = list(set([generation_ranking["generation"] for generation_ranking in generation_rankings]))
    return Response(
        # fmt: off
        data={
            "detail": "기수별 랭킹 조회를 성공했습니다.",
            "data": {
                "generation_rankings": [
                    {
                        "generation": f"{generation}기",
                        "ranking": RankingSerializer(
                            generation_rankings.filter(generation=generation) .order_by("-score"),
                            many=True
                        ).data
                    } for generation in generations
                ],
            },
        },
        status=status.HTTP_200_OK
        # fmt: on
    )
