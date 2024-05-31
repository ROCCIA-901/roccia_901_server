import pytest
from rest_framework import status


@pytest.mark.django_db
class TestAccountEndpoints:

    def test_user_registration(self, api_client, mock_cache, mock_exists):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        response = api_client.post(
            "/api/accounts/register/",
            data={
                "email": "test@gmail.com",
                "password": "Asdf1234!",
                "password_confirmation": "Asdf1234!",
                "username": "홍길동",
                "generation": "8기",
                "role": "운영진",
                "workout_location": "더클라임 양재",
                "workout_level": "파란색",
                "profile_number": 1,
                "introduction": "안녕하세요",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["detail"] == "회원가입에 성공했습니다. 관리자에게 승인 문의 바랍니다."
        assert "user" in response.data["data"]
        assert response.data["data"]["user"]["email"] == "test@gmail.com"
        assert response.data["data"]["user"]["username"] == "홍길동"
