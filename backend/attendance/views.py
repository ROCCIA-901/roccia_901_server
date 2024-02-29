from typing import Any, Optional

from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from account.models import User
from attendance.models import Attendance, AttendanceStats
from attendance.serializers import AttendanceSerializer
from config.exceptions import (
    InternalServerException,
    InvalidFieldException,
    InvalidFieldStateException,
    NotExistException,
)
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
        serializer: AttendanceSerializer = AttendanceSerializer(data=request_data)
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


class AttendanceRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Attendance.objects.filter(request_processed_status=None)
    serializer_class = AttendanceSerializer

    @action(detail=True, methods=["patch"])
    def accept(self, request: Request, pk=None, *args: Any, **kwargs: Any) -> Response:
        attendance_object: Optional[Attendance] = Attendance.objects.filter(id=pk).first()

        if not attendance_object:
            raise NotExistException()

        if attendance_object.request_processed_status is not None:
            raise InvalidFieldStateException("이미 처리된 요청입니다.")

        attendance_object.request_processed_status = "승인"
        attendance_object.request_processed_time = timezone.now()
        attendance_object.request_processed_user = request.user
        # attendance_object.attendance_status = check_attendance_status()
        attendance_object.save()

        return Response(
            # fmt: off
            data={
                "detail": "요청 승인이 성공적으로 완료되었습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )

    @action(detail=True, methods=["patch"])
    def reject(self, request: Request, pk=None, *args: Any, **kwargs: Any) -> Response:
        attendance_object: Optional[Attendance] = Attendance.objects.filter(id=pk).first()

        if not attendance_object:
            raise NotExistException()

        if attendance_object.request_processed_status is not None:
            raise InvalidFieldStateException("이미 처리된 요청입니다.")

        attendance_object.request_processed_status = "거절"
        attendance_object.request_processed_time = timezone.now()
        attendance_object.request_processed_user = request.user
        attendance_object.save()

        return Response(
            # fmt: off
            data={
                "detail": "요청 거절이 성공적으로 완료되었습니다.",
            },
            status=status.HTTP_200_OK
            # fmt: on
        )


class AttendanceUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsMember]

    def get_formatted_dates(self, id: int, status: str):
        dates: QuerySet[Attendance] = Attendance.objects.filter(
            Q(user_id=id) & Q(attendance_status=status)
        ).values_list("request_processed_time", flat=True)
        return [date.strftime("%Y-%m-%d") for date in dates]  # type: ignore

    @action(detail=True, methods=["get"])
    def rate(self, request: Request, pk=None) -> Response:
        attendance_stats_object: Optional[AttendanceStats] = AttendanceStats.objects.filter(user_id=pk).first()

        if not User.objects.filter(id=pk).exists():
            raise NotExistException("존재하지 않는 사용자입니다.")

        if not attendance_stats_object:
            raise NotExistException("해당 사용자에 대한 통계가 존재하지 않습니다.")

        return Response(
            # fmt: off
            data={
                "detail": "사용자 출석률 조회를 성공했습니다.",
                "data": {
                    "attendance_rate": attendance_stats_object.attendance_rate
                }
            },
            status=status.HTTP_200_OK
            # fmt: on
        )

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        pk: Optional[int] = kwargs.get("pk")
        if pk is None:
            raise InvalidFieldException()

        if not User.objects.filter(id=pk).exists():
            raise NotExistException("존재하지 않는 사용자입니다.")

        attendance_list: list = self.get_formatted_dates(pk, "출석") + self.get_formatted_dates(pk, "대체 출석")
        late_list: list = self.get_formatted_dates(pk, "지각")

        return Response(
            # fmt: off
            data={
                "detail": "출석 현황 조회를 성공했습니다.",
                "data": {
                    "attendance": attendance_list,
                    "late": late_list
                }
            },
            status=status.HTTP_200_OK
            # fmt: on
        )
