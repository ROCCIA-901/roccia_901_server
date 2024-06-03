import pytest
from rest_framework import status


@pytest.mark.django_db
class TestMyageEndpoints:

    @pytest.fixture(autouse=True)
    def setup(self, default_user, api_client):
        self.api_client = api_client
        self.default_user = default_user
        login_res = self.api_client.post(
            "/api/accounts/login/",
            data={"email": "defaultuser@example.com", "password": "Password1!"},
            format="json",
        )
        assert login_res.status_code == status.HTTP_200_OK, login_res.data
        self.access_token = login_res.data["data"]["token"]["access"]

    def test_retrieve_mypage_without_user_id(self):
        response = self.api_client.get(
            "/api/mypages/",
            headers={"Authorization": f"Bearer {self.access_token}"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "마이페이지 조회를 성공했습니다."
        assert "profile" in response.data["data"]
        assert "total_workout_time" in response.data["data"]
        assert "records" in response.data["data"]

    def test_retrieve_mypage_with_user_id(self):
        response = self.api_client.get(
            "/api/mypages/",
            data={"user_id": self.default_user.id},
            headers={"Authorization": f"Bearer {self.access_token}"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "마이페이지 조회를 성공했습니다."

    def test_partial_update_mypage(self):
        response = self.api_client.patch(
            "/api/mypages/",
            data={
                "workout_location": "더클라임 연남",
                "workout_level": "파란색",
                "profile_number": "2",
                "introduction": "반갑습니다",
            },
            headers={"Authorization": f"Bearer {self.access_token}"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "사용자 정보 수정을 성공했습니다."
