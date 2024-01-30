from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)

        return Response(
            {
                "message": "회원가입에 성공했습니다.",
                "data": {
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                }
            },
            status=status.HTTP_201_CREATED,
        )
