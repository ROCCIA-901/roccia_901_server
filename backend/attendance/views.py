from typing import Any

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from account.models import User
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from config.exceptions import InternalServerException
from config.utils import IsManager, IsMember


class AttendanceViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsMember]
        else:
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user: User = request.user
        # 해당 일에 아직 처리되지 않은 출석 요청이 존재하고, 현재 들어온 요청보다 먼저 요청 됐으면 예외 처리
        # 출석 누른 시간과 날짜 등을 검증하는 로직
        # 해당 날짜를 기반으로 운동 지점과 주차를 계산하여 필드에 넣어주는 로직 추후에 작성 필요

        # fmt: off
        request_data: dict[str, Any] = {
            "user": user,  # type: ignore
            "request_time": timezone.now(),
            "workout_location": None,
            "week": None,
        }
        # fmt: on
        serializer = AttendanceSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(
            # fmt: off
            data={
                "detail": "출석 요청이 정상적으로 처리됐습니다.",
            },
            status=status.HTTP_201_CREATED
            # fmt: on
        )

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            queryset = Attendance.objects.select_related("user").filter(request_processed_status=None)
            serializer = AttendanceSerializer(queryset, many=True, context={"request_type": "attendance_request_list"})

            return Response(
                # fmt: off
                data={
                    "detail": "출석 요청 목록 조회를 성공했습니다.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
                # fmt: on
            )
        except Exception as e:
            raise InternalServerException()
