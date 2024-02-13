from account.serializers import UserRegistrationSerializer, UserLoginSerializer
from config.exceptions import TokenIssuanceException
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        try:
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)
        except TokenError as e:
            raise TokenIssuanceException({"message": "토큰 발급 중에 문제가 발생했습니다."})

        return Response(
            data={
                "message": "회원가입에 성공했습니다.",
                "data": {
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.validated_data["user"]
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)
        except TokenError as e:
            raise TokenIssuanceException({"message": "토큰 발급 중에 문제가 발생했습니다."})

        return Response(
            data={
                "message": "로그인에 성공했습니다.",
                "data": {
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            },
            status=status.HTTP_200_OK
        )
