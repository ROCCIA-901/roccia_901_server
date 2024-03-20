from typing import Any, Dict, List

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from ranking.models import Ranking
from ranking.serializers import RankingSerializer


class RankingViewSet(viewsets.ModelViewSet):
    allowed_methods = ["get"]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer

    def list(self, request):
        weeks: List[int] = list(set(list(Ranking.objects.values_list("week", flat=True))))
        weeks.sort()
        data: List[Dict] = list()
        for week in weeks:
            weekly_ranking: Dict[str, Any] = dict()
            weekly_ranking["week"] = week
            weekly_ranking["ranking"] = self.serializer_class(Ranking.objects.filter(week=week).all(), many=True).data
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
