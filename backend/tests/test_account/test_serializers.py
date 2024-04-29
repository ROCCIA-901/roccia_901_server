import pytest

from account.models import User
from account.serializers import UserLoginSerializer, UserRegistrationSerializer
from config.exceptions import (
    InvalidAccountException,
    InvalidFieldException,
    InvalidFieldStateException,
)

pytestmark = pytest.mark.unit


class TestUserRegistrationSerializer:

    def test_user_registration_serializer_with_valid_data(self, user_data, mock_cache, mock_exists):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        serializer = UserRegistrationSerializer(data=user_data)
        assert serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        assert validated_data["email"] == user_data["email"]
        assert validated_data["username"] == user_data["username"]
        assert validated_data["generation"] == user_data["generation"]
        assert validated_data["role"] == user_data["role"]
        assert validated_data["workout_location"] == user_data["workout_location"]
        assert validated_data["introduction"] == user_data["introduction"]
        assert type(validated_data["workout_level"]) is int
        assert type(validated_data["password"]) is str

    def test_duplicate_email_validation(self, user_data, mock_cache, mock_exists):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        serializer = UserRegistrationSerializer(data=user_data)
        assert serializer.is_valid(raise_exception=True)

        mock_exists.return_value = True

        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(InvalidFieldException):
            serializer.is_valid(raise_exception=True)

    def test_uncertified_email_validation(self, user_data, mock_cache, mock_exists):
        mock_cache.return_value = "uncertified"
        mock_exists.return_value = False

        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(InvalidFieldStateException):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize("username", ["GILDONG HONG", "홍길동12", "", None])
    def test_username_validation(self, user_data, mock_cache, mock_exists, username):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        user_data["username"] = username
        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize("generation", ["100기", "", None])
    def test_generation_validation(self, user_data, mock_cache, mock_exists, generation):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        user_data["generation"] = generation
        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize("role", ["매니저", "", None])
    def test_role_validation(self, user_data, mock_cache, mock_exists, role):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        user_data["role"] = role
        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize("workout_location", ["피커스 구로", "", None])
    def test_workout_location_validation(self, user_data, mock_cache, mock_exists, workout_location):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        user_data["workout_location"] = workout_location
        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize("workout_level", ["하늘색", "", None])
    def test_workout_level_validation(self, user_data, mock_cache, mock_exists, workout_level):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        user_data["workout_level"] = workout_level
        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize("profile_number", [10, "", None])
    def test_profile_number_validation(self, user_data, mock_cache, mock_exists, profile_number):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        user_data["profile_number"] = profile_number
        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize(
        "password, password_confirmation",
        [
            ("", ""),
            ("Password1!", "WrongPassword1!"),
            ("Pswd1!", "Pswd1!"),
            ("password1!", "password1!"),
            ("PASSWORD1!", "PASSWORD1!"),
            ("Password!", "WrongPassword!"),
            ("Password1", "WrongPassword1"),
            ("패스워드1!", "패스워드1!"),
        ],
    )
    def test_password_validation(self, user_data, mock_cache, mock_exists, password, password_confirmation):
        mock_cache.return_value = "certified"
        mock_exists.return_value = False

        user_data["password"] = password
        user_data["password_confirmation"] = password_confirmation
        serializer = UserRegistrationSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)


class TestUserLoginSerializer:

    def test_user_login_serializer_with_valid_data(self, user_login_data, mock_exists, mock_authenticate):
        mock_exists.return_value = True
        mock_authenticate.return_value = User(email="test@example.com")

        serializer = UserLoginSerializer(data=user_login_data)
        assert serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        assert validated_data["email"] == "test@example.com"
        assert validated_data["password"] == "Password1!"

        mock_authenticate.assert_called_once_with(email="test@example.com", password="Password1!")

    def test_user_login_with_existing_email(self, mock_exists, user_login_data):
        mock_exists.return_value = False

        serializer = UserLoginSerializer(data=user_login_data)
        with pytest.raises(InvalidAccountException):
            serializer.is_valid(raise_exception=True)

    def test_user_login_with_wrong_account(self, mock_exists, user_login_data, mock_authenticate):
        mock_exists.return_value = True
        mock_authenticate.return_value = None

        serializer = UserLoginSerializer(data=user_login_data)
        with pytest.raises(InvalidFieldException):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize(
        "email, password",
        [
            ("", ""),
            (None, ""),
            ("", None),
            (None, None),
        ],
    )
    def test_user_login_with_empty_or_none_field(self, mock_exists, mock_authenticate, email, password):
        mock_exists.return_value = False
        mock_authenticate.return_value = User()

        user_data = {"email": email, "password": password}
        serializer = UserLoginSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)
