from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
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
                status=status.HTTP_200_OK,
            )
