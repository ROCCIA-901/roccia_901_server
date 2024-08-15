from typing import Any, Optional

from django.db import transaction
from django.db.models import F, Q
from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from account.models import User
from attendance.models import (
    Attendance,
    AttendanceStats,
    UnavailableDates,
    WeeklyStaffInfo,
)
from attendance.serializers import (
    AttendanceDetailSerializer,
    AttendanceSerializer,
    UserListSerializer,
)
from attendance.services import (
    check_alternate_attendance,
    get_activity_date,
    get_attendance_status,
    get_current_generation,
    get_day_of_week,
    get_weeks_since_start,
)
from config.exceptions import (
    AttendancePeriodException,
    DuplicateAttendanceException,
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
        current_date = timezone.now().date()

        activity_date = get_activity_date()
        if not activity_date:
            raise AttendancePeriodException()

        current_generation = get_current_generation()
        if current_generation is None:
            raise AttendancePeriodException()

        week = get_weeks_since_start(activity_date.start_date)
        day_of_week = get_day_of_week(current_date)
        workout_location = WeeklyStaffInfo.objects.get(
            generation=current_generation, day_of_week=day_of_week
        ).workout_location

        if Attendance.objects.filter(
            user=user, generation=current_generation, week=week, request_processed_status__in=["대기", "승인"]
        ).exists():
            raise DuplicateAttendanceException()

        if UnavailableDates.objects.filter(date=current_date).exists():
            raise AttendancePeriodException()

        # fmt: off
        request_data: dict[str, Any] = {
            "user": user,
            "generation": current_generation,
            "request_time": timezone.now(),
            "workout_location": workout_location,
            "week": week,
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
            queryset = Attendance.objects.select_related("user").filter(
                request_processed_status="대기", attendance_status=None
            )
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
    def accept(self, request: Request, pk: Optional[int] = None, *args: Any, **kwargs: Any) -> Response:
        with transaction.atomic():
            current_user = request.user
            attendance_object: Optional[Attendance] = Attendance.objects.select_for_update().filter(id=pk).first()

            if not attendance_object:
                raise NotExistException()

            if attendance_object.request_processed_status != "대기":
                raise InvalidFieldStateException("이미 처리된 요청입니다.")

            # 출석 승인 처리 로직
            attendance_status = get_attendance_status()

            attendance_object.request_processed_status = "승인"
            attendance_object.request_processed_time = timezone.now()
            attendance_object.request_processed_user = current_user
            attendance_object.attendance_status = attendance_status

            if check_alternate_attendance(current_user.workout_location):
                attendance_object.is_alternate = True

            attendance_object.save()

            # AttendanceStats 업데이트 로직
            attendance_stats, created = AttendanceStats.objects.select_for_update().get_or_create(
                user=current_user, generation=attendance_object.generation, defaults={"attendance_rate": 0.0}
            )

            if attendance_status == "출석":
                attendance_stats.attendance = F("attendance") + 1
            elif attendance_status == "지각":
                attendance_stats.late = F("late") + 1

            attendance_stats.save()

        return Response(
            data={
                "detail": "요청 승인이 성공적으로 완료되었습니다.",
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["patch"])
    def reject(self, request: Request, pk: Optional[int] = None, *args: Any, **kwargs: Any) -> Response:
        attendance_object: Optional[Attendance] = Attendance.objects.filter(id=pk).first()

        if not attendance_object:
            raise NotExistException()

        if attendance_object.request_processed_status != "대기":
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
    permission_classes = [IsAuthenticated]

    def get_formatted_dates(self, id: int, status: str):
        dates: QuerySet[Attendance] = Attendance.objects.filter(
            Q(user_id=id) & Q(attendance_status=status)
        ).values_list("request_processed_time", flat=True)
        return [date.strftime("%Y-%m-%d") for date in dates]  # type: ignore

    @action(detail=True, methods=["get"])
    def rate(self, request: Request, pk: Optional[int] = None) -> Response:
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
                    "attendance_rate": None
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

    @action(detail=True, methods=["get"], url_path="details")
    def details(self, request: Request, pk: Optional[int] = None) -> Response:
        attendance_stats_obj: Optional[AttendanceStats] = AttendanceStats.objects.filter(user_id=pk).first()
        if not attendance_stats_obj:
            raise NotExistException("존재하지 않는 사용자입니다.")

        attendance_stats_dict: dict[str, int] = {
            "attendance": attendance_stats_obj.attendance,
            "late": attendance_stats_obj.late,
            "absence": attendance_stats_obj.absence,
            # "substitute": attendance_stats_obj.substitute,
        }

        attendance_obj = Attendance.objects.filter(user_id=pk).order_by("week")
        attendance_detail_serializer = AttendanceDetailSerializer(attendance_obj, many=True)

        return Response(
            # fmt: off
            data={
                "detail": "출석 현황 조회를 성공했습니다.",
                "data": {
                    "count": attendance_stats_dict,
                    "detail": attendance_detail_serializer.data
                }
            },
            status=status.HTTP_200_OK
            # fmt: on
        )

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = User.objects.all().prefetch_related("attendance_stats")
        serializer = UserListSerializer(queryset, many=True)

        return Response(
            # fmt: off
            data={
                "detail": "부원 목록 조회를 성공했습니다.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
            # fmt: on
        )
