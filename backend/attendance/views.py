from datetime import date, datetime
from typing import Any, Optional

from django.db import OperationalError, transaction
from django.db.models import F, Q, QuerySet
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
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
from attendance.schemas import (
    APPROVAL_SUCCESS_EXAMPLE,
    ATTENDANCE_PERIOD_INVALID_EXAMPLE,
    ATTENDANCE_RATE_SUCCESS_EXAMPLE,
    ATTENDANCE_RECORD_SUCCESS_EXAMPLE,
    ATTENDANCE_REQUEST_LIST_SUCCESS_EXAMPLE,
    ATTENDANCE_REQUEST_SUCCESS_EXAMPLE,
    ATTENDANCE_STATUS_SUCCESS_EXAMPLE,
    DUPLICATE_ATTENDANCE_EXAMPLE,
    INTERNAL_SERVER_ERROR_EXAMPLE,
    INVALID_ACCOUNT_EXAMPLE,
    INVALID_FIELD_STATE_EXAMPLE,
    LATEST_GENERATION_SUCCESS_EXAMPLE,
    NOT_EXIST_EXAMPLE,
    PERMISSION_DENIED_EXAMPLE,
    REJECTION_SUCCESS_EXAMPLE,
    RESOURCE_LOCKED_EXAMPLE,
    USER_LIST_SUCCESS_EXAMPLE,
    WORKOUT_LOCATION_SUCCESS_EXAMPLE,
    ApprovalResponseSerializer,
    AttendanceRateResponseSerializer,
    AttendanceRecordResponseSerializer,
    AttendanceRequestListResponseSerializer,
    AttendanceStatusResponseSerializer,
    ErrorResponseSerializer,
    RejectionResponseSerializer,
    UserListResponseSerializer,
    WorkoutLocationResponseSerializer,
)
from attendance.serializers import (
    AttendanceDetailSerializer,
    AttendanceRequestListSerializer,
    AttendanceRequestSerializer,
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
    InvalidFieldStateException,
    NotExistException,
    ResourceLockedException,
)
from config.utils import IsManager, IsMember


class AttendanceAPIView(APIView):
    """
    출석 요청과 출석 현황 조회를 위한 클래스입니다.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsMember()]
        return []

    @extend_schema(
        tags=["출석"],
        summary="출석 현황 조회",
        description="사용자의 출석 현황을 조회합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AttendanceStatusResponseSerializer,
                examples=[ATTENDANCE_STATUS_SUCCESS_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        current_user: User = request.user

        attendance_dates: list[datetime] = list(
            Attendance.objects.filter(
                Q(user=current_user) & Q(attendance_status__in=["출석", "대체 출석"])
            ).values_list("request_time", flat=True)
        )

        late_dates: list[datetime] = list(
            Attendance.objects.filter(Q(user=current_user) & Q(attendance_status="지각")).values_list(
                "request_time", flat=True
            )
        )

        attendance_list: list[str] = [date.strftime("%Y-%m-%d") for date in attendance_dates]
        late_list: list[str] = [date.strftime("%Y-%m-%d") for date in late_dates]

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

    @extend_schema(
        tags=["출석"],
        summary="출석 요청",
        description="사용자의 출석 요청을 처리합니다.",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=AttendanceRequestSerializer,
                examples=[ATTENDANCE_REQUEST_SUCCESS_EXAMPLE],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[
                    ATTENDANCE_PERIOD_INVALID_EXAMPLE,
                    DUPLICATE_ATTENDANCE_EXAMPLE,
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
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
            raise AttendancePeriodException()

        if UnavailableDates.objects.filter(date=current_date).exists():
            raise AttendancePeriodException()

        if Attendance.objects.filter(
            user=user, generation=current_generation, week=week, request_processed_status__in=["대기", "승인"]
        ).exists():
            raise DuplicateAttendanceException()

        request_data: dict[str, Any] = {
            "user": user.id,  # type: ignore
            "generation": current_generation.name,
            "request_time": timezone.now(),
            "workout_location": weekly_staff_info.workout_location,
            "week": week,
        }
        serializer: AttendanceRequestSerializer = AttendanceRequestSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "detail": "출석 요청이 정상적으로 처리됐습니다.",
            },
            status=status.HTTP_201_CREATED,
        )


class AttendanceRequestListAPIView(APIView):
    """
    출석 요청 목록 조회를 위한 클래스입니다.
    """

    permission_classes = [IsManager]

    @extend_schema(
        tags=["출석"],
        summary="출석 요청 목록 조회",
        description="처리 대기 중인 출석 요청 목록을 조회합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AttendanceRequestListResponseSerializer,
                examples=[ATTENDANCE_REQUEST_LIST_SUCCESS_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        attendance: QuerySet[Attendance] = Attendance.objects.select_related("user").filter(
            request_processed_status="대기", attendance_status=None
        )
        serializer: AttendanceRequestListSerializer = AttendanceRequestListSerializer(attendance, many=True)

        return Response(
            data={
                "detail": "출석 요청 목록 조회를 성공했습니다.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AttendanceAcceptAPIView(APIView):
    """
    출석 승인 처리를 위한 클래스입니다.
    """

    permission_classes = [IsManager]

    @extend_schema(
        tags=["출석"],
        summary="출석 요청 승인",
        description="특정 출석 요청을 승인 처리합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ApprovalResponseSerializer,
                examples=[APPROVAL_SUCCESS_EXAMPLE],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_FIELD_STATE_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[NOT_EXIST_EXAMPLE],
            ),
            status.HTTP_423_LOCKED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[RESOURCE_LOCKED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
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
            attendance.is_alternate = check_alternate_attendance(attendance.user)

            attendance.save()

            # AttendanceStats 업데이트 로직
            attendance_stats, created = AttendanceStats.objects.select_for_update(nowait=True).get_or_create(
                user=attendance.user,
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

    @extend_schema(
        tags=["출석"],
        summary="출석 요청 거절",
        description="특정 출석 요청을 거절 처리합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=RejectionResponseSerializer,
                examples=[REJECTION_SUCCESS_EXAMPLE],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_FIELD_STATE_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[NOT_EXIST_EXAMPLE],
            ),
            status.HTTP_423_LOCKED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[RESOURCE_LOCKED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
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


class AttendanceRateAPIView(APIView):
    """
    출석률 조회를 위한 클래스입니다.
    """

    permission_classes = [IsMember]

    @extend_schema(
        tags=["출석"],
        summary="사용자 출석률 조회",
        description="현재 사용자의 출석률을 조회합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AttendanceRateResponseSerializer,
                examples=[ATTENDANCE_RATE_SUCCESS_EXAMPLE],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[ATTENDANCE_PERIOD_INVALID_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        current_user: User = request.user

        current_generation: Generation = get_current_generation()
        if current_generation is None:
            raise AttendancePeriodException()
        attendance_stats: Optional[AttendanceStats] = AttendanceStats.objects.filter(
            user=current_user, generation=current_generation
        ).first()

        attendance_rate: float = 0
        if attendance_stats:
            current_gen_number: int = int(current_generation.name[:-1])
            user_gen_number: int = int(current_user.generation.name[:-1])
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


class AttendanceDetailAPIView(APIView):
    """
    출석 내역 조회를 위한 클래스입니다.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["출석"],
        summary="사용자 출석 내역 조회",
        description="특정 사용자의 현재 기수에 대한 출석 내역을 조회합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AttendanceRecordResponseSerializer,
                examples=[ATTENDANCE_RECORD_SUCCESS_EXAMPLE],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[ATTENDANCE_PERIOD_INVALID_EXAMPLE],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[NOT_EXIST_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request, user_id: int) -> Response:
        if not User.objects.filter(id=user_id).exists():
            raise NotExistException("존재하지 않는 사용자입니다.")

        current_generation: Generation = get_current_generation()
        if current_generation is None:
            raise AttendancePeriodException()

        attendance_stats: Optional[AttendanceStats] = AttendanceStats.objects.filter(
            user_id=user_id, generation=current_generation
        ).first()

        attendance_queryset: QuerySet[Attendance] = Attendance.objects.filter(
            user_id=user_id, generation=current_generation
        ).order_by("week")

        alternative_count: int = attendance_queryset.filter(is_alternate=True).count()

        attendance_stats_dict: dict[str, int] = {
            "attendance": attendance_stats.attendance if attendance_stats else 0,
            "late": attendance_stats.late if attendance_stats else 0,
            "absence": attendance_stats.absence if attendance_stats else 0,
            "alternative": 2 - alternative_count,
        }

        processed_attendance_queryset: QuerySet[Attendance] = attendance_queryset.filter(
            attendance_status__isnull=False
        )
        attendance_detail_serializer: AttendanceDetailSerializer = AttendanceDetailSerializer(
            processed_attendance_queryset, many=True
        )

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


class AttendanceLocationAPIView(APIView):
    """
    운동 지점 조회를 위한 클래스입니다.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["출석"],
        summary="금일 운동 지점 조회",
        description="현재 날짜의 운동 지점을 조회합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=WorkoutLocationResponseSerializer,
                examples=[WORKOUT_LOCATION_SUCCESS_EXAMPLE],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[ATTENDANCE_PERIOD_INVALID_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        try:
            day_of_week: str = get_day_of_week(timezone.now())
            current_generation: Generation = get_current_generation()
            weekly_staff_info: Optional[WeeklyStaffInfo] = WeeklyStaffInfo.objects.get(
                generation=current_generation, day_of_week=day_of_week
            )
            workout_location: str = weekly_staff_info.workout_location  # type: ignore

            return Response(
                data={
                    "detail": "금일 운동 지점 조회를 성공했습니다.",
                    "data": {
                        "workout_location": workout_location,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            raise AttendancePeriodException()


class AttendanceUserListAPIView(APIView):
    """
    부원 목록 조회를 위한 클래스입니다.
    """

    permission_classes = [IsManager]

    @extend_schema(
        tags=["출석"],
        summary="부원 목록 조회",
        description="현재 활성화된 부원들의 목록을 조회하며, 각 부원의 출석률과 운동 수준을 포함합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserListResponseSerializer,
                examples=[USER_LIST_SUCCESS_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[PERMISSION_DENIED_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        queryset: QuerySet = User.objects.filter(role="부원", is_active=True).all()
        serializer: UserListSerializer = UserListSerializer(queryset, many=True)

        return Response(
            data={
                "detail": "부원 목록 조회를 성공했습니다.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AttendanceLatestGenerationAPIView(APIView):
    """
    최근 기수 조회를 위한 클래스입니다.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["출석"],
        summary="최근 기수 조회",
        description="최근 기수를 조회합니다.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserListResponseSerializer,
                examples=[LATEST_GENERATION_SUCCESS_EXAMPLE],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INVALID_ACCOUNT_EXAMPLE],
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=[INTERNAL_SERVER_ERROR_EXAMPLE],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        generation_object = Generation.objects.filter(start_date__isnull=False).order_by("-start_date").first()

        latest_generation = None
        if generation_object:
            latest_generation = int(generation_object.name[:-1])

        return Response(
            data={
                "detail": "최근 기수 조회를 성공했습니다.",
                "data": {
                    "generation": latest_generation,
                },
            },
            status=status.HTTP_200_OK,
        )
