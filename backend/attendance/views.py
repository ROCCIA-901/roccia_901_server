from datetime import datetime
from typing import Any

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from attendance.serializers import AttendanceSerializer
from config.utils import IsMember


class AttendanceRequest(APIView):
    permission_classes = [IsMember]

    def post(self, request: Request) -> Response:
        user: User = request.user
        # 해당 일에 아직 처리되지 않은 출석 요청이 존재하고, 현재 들어온 요청보다 먼저 요청 됐으면 예외 처리
        # 출석 누른 시간과 날짜 등을 검증하는 로직
        # 해당 날짜를 기반으로 운동 지점과 주차를 계산하여 필드에 넣어주는 로직 추후에 작성 필요

        # fmt: off
        request_data: dict[str, Any] = {
            "user_id": user.id,  # type: ignore
            "request_time": datetime.now(),
            "workout_location": None,
            "week": None,
        }
        # fmt: on
        serializer = AttendanceSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            # fmt: off
            data={
                "detail": "출석 요청이 정상적으로 처리됐습니다.",
            },
            status=status.HTTP_201_CREATED
            # fmt: on
        )
