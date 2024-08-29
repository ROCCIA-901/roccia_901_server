from datetime import datetime
from typing import Dict, List, Optional

from django.db import models
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from account.models import Generation
from attendance.services import get_current_generation
from ranking.models import Ranking
from ranking.schemas import (
    RANKING_401_FAILURE_EXAMPLE,
    RANKING_500_FAILURE_EXAMPLE,
    RANKING_GENERATIONS_RESPONSE_EXAMPLE,
    RANKING_WEEKS_RESPONSE_EXAMPLE,
    ErrorResponseSerializer,
)
from ranking.serializers import RankingSerializer
from ranking.services import get_weeks_in_generation


@extend_schema(
    tags=["랭킹"],
    summary="주차별 랭킹 조회",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=RankingSerializer,
            examples=RANKING_WEEKS_RESPONSE_EXAMPLE,
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_401_FAILURE_EXAMPLE,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_500_FAILURE_EXAMPLE,
        ),
    },
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_weekly_rankings(request: Request) -> Response:
    today = datetime.now().date()
    cur_generation: Optional[Generation] = Generation.objects.filter(start_date__lte=today, end_date__gte=today).first()

    if cur_generation:
        weeks = (
            Ranking.objects.filter(generation=cur_generation).values_list("week", flat=True).distinct().order_by("week")
        )
        data: List[Dict] = []
        for week in weeks:
            weekly_ranking = {
                "week": week,
                "ranking": RankingSerializer(
                    Ranking.objects.filter(generation=cur_generation, week=week)
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
                    "current_generation_week": get_weeks_in_generation(datetime.now().date()),
                    "weekly_rankings": data,
                },
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            data={
                "detail": "주차별 랭킹 목록 조회를 성공했습니다.",
                "data": {
                    "current_generation_week": None,
                    "weekly_rankings": [],
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["랭킹"],
    summary="기수별 랭킹 조회",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=RankingSerializer,
            examples=RANKING_GENERATIONS_RESPONSE_EXAMPLE,
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_401_FAILURE_EXAMPLE,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=ErrorResponseSerializer,
            examples=RANKING_500_FAILURE_EXAMPLE,
        ),
    },
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
    data = {
        "generation_rankings": [
            {
                "generation": generation,
                "ranking": RankingSerializer(
                    generation_rankings.filter(generation=generation).order_by("-score"), many=True
                ).data,
            }
            for generation in generations
        ],
    }
    if len(data["generation_rankings"]) == 0:
        data = {
            "generation_rankings": [
                {
                    "generation": get_current_generation().name,
                    "ranking": [],
                }
            ],
        }
    return Response(
        data={
            "detail": "기수별 랭킹 조회를 성공했습니다.",
            "data": data,
        },
        status=status.HTTP_200_OK,
    )
