from unittest.mock import MagicMock

import pytest

from common.choices import WORKOUT_LEVELS
from config.exceptions import InvalidFieldException
from mypage.serializers import (
    LevelCountSerializer,
    MypageSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)


class TestUserProfileSerializer:
    def test_user_retrieve_serializer(self, mock_user_model):
        serializer = UserProfileSerializer(instance=mock_user_model)
        expected_data = {
            "username": mock_user_model.username,
            "generation": mock_user_model.generation,
            "role": mock_user_model.role,
            "workout_location": mock_user_model.workout_location,
            "workout_level": dict(WORKOUT_LEVELS)[mock_user_model.workout_level],
            "profile_number": mock_user_model.profile_number,
            "introduction": mock_user_model.introduction,
        }

        assert serializer.data == expected_data
        assert serializer.data.keys() == expected_data.keys()


class TestLevelCountSerializer:

    def test_level_count_serializer_serialization(self):
        data = {"workout_level": 1, "total_count": 10}
        serializer = LevelCountSerializer(data)
        assert serializer.data == {"workout_level": "하얀색", "total_count": 10}


class TestMypageSerializer:

    def test_mypage_serializer(self, mock_boulder_problem_object, mock_record_object, mock_user_model):
        mock_boulder_problem_object.return_value.values.return_value.annotate.return_value.order_by.return_value = [
            {"workout_level": 1, "total_count": 10},
            {"workout_level": 2, "total_count": 20},
        ]
        mock_record_object.return_value.annotate.return_value.aggregate.return_value = {
            "total": MagicMock(total_seconds=MagicMock(return_value=330 * 60))
        }
        serializer = MypageSerializer(instance=mock_user_model)
        data = serializer.data

        expected_data = {
            "profile": {
                "username": mock_user_model.username,
                "generation": mock_user_model.generation,
                "role": mock_user_model.role,
                "workout_location": mock_user_model.workout_location,
                "workout_level": dict(WORKOUT_LEVELS)[mock_user_model.workout_level],
                "profile_number": mock_user_model.profile_number,
                "introduction": mock_user_model.introduction,
            },
            "total_workout_time": 330,
            "records": [
                {"workout_level": "하얀색", "total_count": 10},
                {"workout_level": "노란색", "total_count": 20},
            ],
        }

        assert data == expected_data


class TestUserUpdateSerializer:

    @pytest.mark.parametrize(
        "workout_location, workout_level, profile_number",
        [
            ("더클라임 양재", "1", ""),
            ("더클라임 양재", "", "7"),
            ("", "1", "7"),
        ],
    )
    def test_field_verification(self, workout_location, workout_level, profile_number):
        data = {"workout_location": workout_location, "workout_level": workout_level, "profile_number": profile_number}

        serializer = UserUpdateSerializer(data=data)
        with pytest.raises(InvalidFieldException):
            serializer.is_valid(raise_exception=True)

    def test_invalid_workout_location_verification(self):
        data = {"workout_location": "피커스 구로", "workout_level": "파란색", "profile_number": "1"}

        serializer = UserUpdateSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="지점이 정확하지 않습니다."):
            serializer.is_valid(raise_exception=True)

    def test_invalid_workout_level_verification(self):
        data = {"workout_location": "더클라임 양재", "workout_level": "분홍색", "profile_number": "1"}

        serializer = UserUpdateSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="난이도가 정확하지 않습니다."):
            serializer.is_valid(raise_exception=True)

    def test_invalid_profile_number_verification(self):
        data = {"workout_location": "더클라임 양재", "workout_level": "파란색", "profile_number": "100"}

        serializer = UserUpdateSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="프로필 번호가 정확하지 않습니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_success(self):
        data = {"workout_location": "더클라임 양재", "workout_level": "파란색", "profile_number": "5"}

        serializer = UserUpdateSerializer(data=data)
        assert serializer.is_valid()
