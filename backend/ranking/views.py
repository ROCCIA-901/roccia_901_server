from typing import Any, Dict, List

from django.db import models
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from ranking.models import Ranking
from ranking.serializers import RankingSerializer


class WeeklyRankingViewSet(viewsets.ModelViewSet):
    allowed_methods = ["get"]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer  # type: ignore

    def list(self, request: Request) -> Response:  # type: ignore
        weeks: List[int] = list(set(list(Ranking.objects.values_list("week", flat=True))))
        weeks.sort()  # type: ignore
        data: List[Dict] = list()
        for week in weeks:
            weekly_ranking: Dict[str, Any] = dict()
            weekly_ranking["week"] = week
            weekly_ranking["ranking"] = self.serializer_class(
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
            ).data
            data.append(weekly_ranking)
        return Response(
            # fmt: off
            data={
                "detail": "주차별 랭킹 목록 조회를 성공했습니다.",
                "data": data
            },
            status=status.HTTP_200_OK
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
            "data": [
                {
                    "generation": generation,
                    "ranking": RankingSerializer(
                        generation_rankings.filter(generation=generation) .order_by("-score"),
                        many=True
                    ).data
                } for generation in generations
            ]
        },
        status=status.HTTP_200_OK
        # fmt: on
    )
