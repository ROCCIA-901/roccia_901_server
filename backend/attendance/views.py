from datetime import date
from typing import Any, Optional

from django.db import OperationalError, transaction
from django.db.models import F, Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Generation, User
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
    calculate_attendance_rate,
    check_alternate_attendance,
    get_attendance_status,
    get_current_generation,
    get_day_of_week,
    get_weeks_since_start,
)
from config.exceptions import (
    AttendancePeriodException,
    DuplicateAttendanceException,
    InternalServerException,
    InvalidFieldStateException,
    MissingWeeklyStaffInfoException,
    NotExistException,
    ResourceLockedException,
)
from config.utils import IsManager, IsMember


class AttendanceViewSet(viewsets.ModelViewSet):

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self.permission_classes = [IsAuthenticated]

        current_user = request.user

        attendance_dates = Attendance.objects.filter(
            Q(user=current_user) & Q(attendance_status__in=["출석", "대체 출석"])
        ).values_list("request_time", flat=True)

        late_dates = Attendance.objects.filter(Q(user=current_user) & Q(attendance_status="지각")).values_list(
            "request_time", flat=True
        )

        attendance_list = [date.strftime("%Y-%m-%d") for date in attendance_dates]
        late_list = [date.strftime("%Y-%m-%d") for date in late_dates]

        return Response(
            data={
                "detail": "출석 현황 조회를 성공했습니다.",
                "data": {
                    "attendance": attendance_list,
                    "late": late_list,
                },
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], permission_classes=[IsMember])
    def rate(self, request: Request) -> Response:
        current_user = request.user

        current_generation = get_current_generation()
        if current_generation is None:
            raise AttendancePeriodException()
        attendance_stats = AttendanceStats.objects.filter(user=current_user, generation=current_generation).first()

        if not attendance_stats:
            raise NotExistException("해당 사용자에 대한 통계가 존재하지 않습니다.")

        current_gen_number = int(current_generation[:-1])
        user_gen_number = int(current_user.generation[:-1])
        attendance_rate = calculate_attendance_rate(attendance_stats, current_gen_number, user_gen_number)

        return Response(
            data={
                "detail": "사용자 출석률 조회를 성공했습니다.",
                "data": {
                    "attendance_rate": round(attendance_rate, 2),
                },
            },
            status=status.HTTP_200_OK,
        )


class AttendanceRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Attendance.objects.filter(request_processed_status=None)
    serializer_class = AttendanceSerializer

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            queryset = Attendance.objects.select_related("user").filter(
                request_processed_status="대기", attendance_status=None
            )
            serializer = AttendanceSerializer(queryset, many=True, context={"request_type": "attendance_request_list"})

            return Response(
                data={
                    "detail": "출석 요청 목록 조회를 성공했습니다.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            raise InternalServerException()


class AttendanceUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="details")
    def details(self, request: Request, pk: int) -> Response:

        if not User.objects.filter(id=pk).exists():
            raise NotExistException("존재하지 않는 사용자입니다.")

        current_generation = get_current_generation()
        if current_generation is None:
            raise AttendancePeriodException()

        attendance_stats_obj: Optional[AttendanceStats] = AttendanceStats.objects.filter(
            user_id=pk, generation=current_generation
        ).first()

        attendance_obj = Attendance.objects.filter(user_id=pk, generation=current_generation).order_by("week")

        alternative_count = attendance_obj.filter(is_alternate=True).count()

        attendance_stats_dict: dict[str, int] = {
            "attendance": attendance_stats_obj.attendance if attendance_stats_obj else 0,
            "late": attendance_stats_obj.late if attendance_stats_obj else 0,
            "absence": attendance_stats_obj.absence if attendance_stats_obj else 0,
            "alternative": 2 - alternative_count,
        }

        attendance_detail_serializer = AttendanceDetailSerializer(attendance_obj, many=True)

        return Response(
            data={
                "detail": "출석 내역 조회를 성공했습니다.",
                "data": {
                    "count": attendance_stats_dict,
                    "detail": attendance_detail_serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = User.objects.filter(is_active=True).all()
        serializer = UserListSerializer(queryset, many=True)

        return Response(
            data={
                "detail": "부원 목록 조회를 성공했습니다.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AttendanceAPIView(APIView):
    """
    출석 요청과 목록 조회를 위한 클래스입니다.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsMember()]
        return []

    def post(self, request: Request) -> Response:
        user: User = request.user
        current_date: date = timezone.now().date()

        current_generation: Generation = get_current_generation()
        week: int = get_weeks_since_start(current_generation.start_date)
        day_of_week: str = get_day_of_week(current_date)

        weekly_staff_info: Optional[WeeklyStaffInfo] = WeeklyStaffInfo.objects.filter(
            generation=current_generation, day_of_week=day_of_week
        ).first()
        if weekly_staff_info is None:
            raise MissingWeeklyStaffInfoException()

        if Attendance.objects.filter(
            user=user, generation=current_generation, week=week, request_processed_status__in=["대기", "승인"]
        ).exists():
            raise DuplicateAttendanceException()

        if UnavailableDates.objects.filter(date=current_date).exists():
            raise AttendancePeriodException()

        request_data: dict[str, Any] = {
            "user": user.id,  # type: ignore
            "generation": current_generation.name,
            "request_time": timezone.now(),
            "workout_location": weekly_staff_info.workout_location,
            "week": week,
        }
        serializer: AttendanceSerializer = AttendanceSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "detail": "출석 요청이 정상적으로 처리됐습니다.",
            },
            status=status.HTTP_201_CREATED,
        )


class AttendanceAcceptAPIView(APIView):
    """
    출석 승인 처리를 위한 클래스입니다.
    """

    permission_classes = [IsManager]

    @transaction.atomic
    def patch(self, request: Request, attendance_id: int) -> Response:
        try:
            current_user: User = request.user
            attendance: Optional[Attendance] = (
                Attendance.objects.select_for_update(nowait=True).filter(id=attendance_id).first()
            )

            if not attendance:
                raise NotExistException()

            if attendance.request_processed_status != "대기":
                raise InvalidFieldStateException("이미 처리된 요청입니다.")

            # 출석 승인 처리 로직
            attendance_status: str = get_attendance_status(attendance.request_time)

            attendance.request_processed_status = "승인"
            attendance.request_processed_time = timezone.now()
            attendance.request_processed_user = current_user
            attendance.attendance_status = attendance_status
            attendance.is_alternate = check_alternate_attendance(current_user)

            attendance.save()

            # AttendanceStats 업데이트 로직
            attendance_stats, created = AttendanceStats.objects.select_for_update(nowait=True).get_or_create(
                user=current_user,
                generation=attendance.generation,
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
        except OperationalError:
            raise ResourceLockedException()


class AttendanceRejectAPIView(APIView):
    """
    출석 거절 처리를 위한 클래스입니다.
    """

    permission_classes = [IsManager]

    @transaction.atomic
    def patch(self, request: Request, attendance_id: int) -> Response:
        try:
            attendance: Optional[Attendance] = (
                Attendance.objects.select_for_update(nowait=True).filter(id=attendance_id).first()
            )

            if not attendance:
                raise NotExistException()

            if attendance.request_processed_status != "대기":
                raise InvalidFieldStateException("이미 처리된 요청입니다.")

            attendance.request_processed_status = "거절"
            attendance.request_processed_time = timezone.now()
            attendance.request_processed_user = request.user
            attendance.save()

            return Response(
                data={
                    "detail": "요청 거절이 성공적으로 완료되었습니다.",
                },
                status=status.HTTP_200_OK,
            )
        except OperationalError:
            raise ResourceLockedException()


class AttendanceLocationAPIView(APIView):
    """
    운동 지점 조회를 위한 클래스입니다.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        day_of_week: str = get_day_of_week(timezone.now())
        current_generation: Generation = get_current_generation()

        weekly_staff_info: Optional[WeeklyStaffInfo] = WeeklyStaffInfo.objects.filter(
            generation=current_generation, day_of_week=day_of_week
        ).first()

        if not weekly_staff_info:
            raise MissingWeeklyStaffInfoException()

        workout_location: str = weekly_staff_info.workout_location

        return Response(
            data={
                "detail": "금일 운동 지점 조회를 성공했습니다.",
                "data": {
                    "workout_location": workout_location,
                },
            },
            status=status.HTTP_200_OK,
        )
