from django.db.models.functions import TruncDate
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from config.exceptions import PermissionFailedException
from record.models import Record
from record.schemas import (
    RECORD_401_FAILURE_EXAMPLE,
    RECORD_403_FAILURE_EXAMPLE,
    RECORD_500_FAILURE_EXAMPLE,
    RECORD_CREATE_400_FAILURE_EXAMPLE,
    RECORD_CREATE_RESPONSE_EXAMPLE,
    RECORD_DATES_RESPONSE_EXAMPLE,
    RECORD_DESTROY_RESPONSE_EXAMPLE,
    RECORD_LIST_RESPONSE_EXAMPLE,
    RECORD_UPDATE_REQUEST_EXAMPLE,
    RECORD_UPDATE_RESPONSE_EXAMPLE,
    ErrorResponseSerializer,
)
from record.serializers import RecordCreateSerializer, RecordSerializer


@extend_schema_view(
    retrieve=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
class RecordViewSet(viewsets.ModelViewSet):
    allowed_methods = ["get", "post", "put", "delete"]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return RecordCreateSerializer
        return RecordSerializer

    @extend_schema(
        tags=["운동 기록"],
        summary="운동 기록 생성",
        request=RecordCreateSerializer,
        # fmt: off
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=RecordCreateSerializer,
                examples=RECORD_CREATE_RESPONSE_EXAMPLE
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_CREATE_400_FAILURE_EXAMPLE
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_401_FAILURE_EXAMPLE
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_403_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            data={
                "detail": "운동 기록이 생성되었습니다.",
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        tags=["운동 기록"],
        summary="운동 기록 수정",
        parameters=[
            OpenApiParameter(
                name="id", location=OpenApiParameter.PATH, description="수정할 기록의 ID", required=True, type=int
            ),
        ],
        request=RecordSerializer,
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=RecordSerializer,
                examples=RECORD_UPDATE_RESPONSE_EXAMPLE
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_401_FAILURE_EXAMPLE
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_403_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
        examples=RECORD_UPDATE_REQUEST_EXAMPLE,
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

    @extend_schema(
        tags=["운동 기록"],
        summary="운동 기록 전체 조회",
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=RecordSerializer,
                examples=RECORD_LIST_RESPONSE_EXAMPLE
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_401_FAILURE_EXAMPLE
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_403_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
    )
    def list(self, request, *args, **kwargs):
        data = Record.objects.filter(user=request.user)  # type: ignore
        data = self.get_serializer(data, many=True).data
        return Response(
            data={
                "detail": "모든 운동 기록을 가져왔습니다.",
                "data": {
                    "records": data,
                },
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["운동 기록"],
        summary="운동 기록 삭제",
        parameters=[
            OpenApiParameter(
                name="id", location=OpenApiParameter.PATH, description="삭제할 기록의 ID", required=True, type=int
            ),
        ],
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=RecordSerializer,
                examples=RECORD_DESTROY_RESPONSE_EXAMPLE
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_401_FAILURE_EXAMPLE
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_403_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
    )
    def destroy(self, request, *args, **kwargs):
        if self.request.user != self.get_object().user:
            raise PermissionFailedException

        super().destroy(request, *args, **kwargs)
        return Response(
            data={
                "detail": "운동 기록이 삭제되었습니다.",
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["운동 기록"],
        summary="운동 기록 날짜 조회",
        # fmt: off
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_DATES_RESPONSE_EXAMPLE
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_401_FAILURE_EXAMPLE
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorResponseSerializer,
                examples=RECORD_500_FAILURE_EXAMPLE
            ),
        },
        # fmt: on
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
