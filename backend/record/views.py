from django.db.models.functions import TruncDate
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from record.models import Record
from record.serializers import RecordCreateSerializer, RecordSerializer


# TODO: 생성, 수정 권한 일치해야지만 가능하게 수정
class RecordViewSet(viewsets.ModelViewSet):
    allowed_methods = ["get", "post", "put", "delete"]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_serializer_class(self):
        if self.action == "list" or "retrieve":
            return RecordSerializer
        return RecordCreateSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            data={
                "detail": "운동 기록이 생성되었습니다.",
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            return Response(
                data={
                    "detail": "운동 기록을 수정할 권한이 없습니다.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        super().update(request, *args, **kwargs)
        return Response(
            data={
                "detail": "운동 기록이 수정되었습니다.",
            },
            status=status.HTTP_200_OK,
        )

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)
        return Response(
            data={
                "detail": "모든 운동 기록을 가져왔습니다.",
                "data": {
                    "records": data.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            return Response(
                data={
                    "detail": "운동 기록을 삭제할 권한이 없습니다.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        super().destroy(request, *args, **kwargs)
        return Response(
            data={
                "detail": "운동 기록이 삭제되었습니다.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["get"], url_path="dates")
    def dates(self, request: Request) -> Response:
        dates = (
            Record.objects.filter(user=request.user)
            .annotate(date=TruncDate("start_time"))
            .values_list("date", flat=True)
            .order_by("date")
            .all()
        )

        return Response(
            # fmt: off
            data={
                "detail": "운동 기록 날짜 목록 조회를 성공했습니다.",
                "data": {
                    "dates": dates,
                },
            },
            status=status.HTTP_200_OK
            # fmt: on
        )
