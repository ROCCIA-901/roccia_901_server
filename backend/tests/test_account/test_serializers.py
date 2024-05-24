import pytest
from rest_framework.exceptions import ValidationError

from account.models import User
from account.serializers import (
    CustomTokenRefreshSerializer,
    PasswordUpdateAuthCodeVerificationSerializer,
    PasswordUpdateEmailVerificationSerializer,
    UserLoginSerializer,
    UserRegisterAuthCodeVerificationSerializer,
    UserRegisterEmailVerificationSerializer,
    UserRegistrationSerializer,
    UserRetrieveSerializer,
)
from config.exceptions import (
    InvalidAccountException,
    InvalidFieldException,
    InvalidFieldStateException,
    InvalidRefreshTokenException,
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
            ("1234567!", "1234567!"),
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

    def test_user_login_serializer_with_valid_data(
        self, user_login_data, mock_exists, mock_authenticate, mock_active_user_filter_queryset
    ):
        mock_exists.return_value = True
        mock_authenticate.return_value = User(email="test@example.com")
        mock_active_user_filter_queryset.return_value.values_list.return_value.first.return_value = True

        serializer = UserLoginSerializer(data=user_login_data)
        assert serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        assert validated_data["email"] == "test@example.com"
        assert validated_data["password"] == "Password1!"

        mock_authenticate.assert_called_once_with(email="test@example.com", password="Password1!")

    def test_user_login_with_existing_email(self, mock_exists, user_login_data):
        mock_exists.return_value = False

        serializer = UserLoginSerializer(data=user_login_data)
        with pytest.raises(InvalidAccountException, match="등록되지 않은 이메일입니다."):
            serializer.is_valid(raise_exception=True)

    def test_user_login_with_wrong_account(
        self, mock_exists, user_login_data, mock_authenticate, mock_active_user_filter_queryset
    ):
        mock_exists.return_value = True
        mock_authenticate.return_value = None
        mock_active_user_filter_queryset.return_value.values_list.return_value.first.return_value = True

        serializer = UserLoginSerializer(data=user_login_data)
        with pytest.raises(InvalidFieldException, match="이메일 또는 비밀번호가 유효하지 않습니다."):
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

        user_data = {"email": "test@example.com", "password": password}
        serializer = UserLoginSerializer(data=user_data)
        with pytest.raises(Exception):
            serializer.is_valid(raise_exception=True)

    def test_deactivate_user_login(self, mock_exists, mock_authenticate, mock_active_user_filter_queryset):
        mock_exists.return_value = True
        mock_authenticate.return_value = User(email="test@example.com")
        mock_active_user_filter_queryset.return_value.values_list.return_value.first.return_value = False

        user_data = {"email": "test@test.com", "password": "Password1!"}
        serializer = UserLoginSerializer(data=user_data)
        with pytest.raises(InvalidAccountException, match="가입 승인이 필요한 계정입니다. 관리자에게 문의해주세요."):
            serializer.is_valid(raise_exception=True)


class TestUserRetrieveSerializer:
    def test_user_retrieve_serializer(self, mock_user_model):
        serializer = UserRetrieveSerializer(instance=mock_user_model)
        expected_data = {
            "id": mock_user_model.id,
            "email": mock_user_model.email,
            "username": mock_user_model.username,
            "generation": mock_user_model.generation,
            "role": mock_user_model.role,
            "workout_location": mock_user_model.workout_location,
            "workout_level": mock_user_model.workout_level,
            "profile_number": mock_user_model.profile_number,
            "introduction": mock_user_model.introduction,
        }

        assert serializer.data == expected_data
        assert serializer.data.keys() == expected_data.keys()


class TestUserRegisterEmailVerificationSerializer:
    @pytest.mark.parametrize("email", ["", None])
    def test_email_field_verification(self, mock_exists, email):
        mock_exists.return_value = False
        data = {"email": email}

        serializer = UserRegisterEmailVerificationSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_not_exist_email_verification(self, mock_exists):
        mock_exists.return_value = True
        data = {"email": "test@example.com"}

        serializer = UserRegisterEmailVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldException):
            serializer.is_valid(raise_exception=True)

    def test_validate_success(self, mock_exists):
        mock_exists.return_value = False
        data = {"email": "test@example.com"}

        serializer = UserRegisterEmailVerificationSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data


class TestUserRegisterAuthCodeVerificationSerializer:

    @pytest.mark.parametrize(
        "email, code",
        [
            ("", ""),
            (None, ""),
            ("", None),
            (None, None),
        ],
    )
    def test_field_verification(self, email, code):
        data = {"email": email, "code": code}

        serializer = UserRegisterAuthCodeVerificationSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_email_failure(self, mock_cache):
        mock_cache.return_value = False
        data = {"email": "test@example.com", "code": 123456}
        serializer = UserRegisterAuthCodeVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="해당 이메일의 인증번호 요청 내역이 존재하지 않습니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_already_certified(self, mock_cache):
        mock_cache.return_value = "certified"
        data = {"email": "test@example.com", "code": 123456}
        serializer = UserRegisterAuthCodeVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldStateException, match="이미 인증 완료된 사용자입니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_code_mismatch(self, mock_cache):
        mock_cache.side_effect = lambda key: 123456 if key == "test@example.com:register:code" else None
        data = {"email": "test@example.com", "code": 654321}
        serializer = UserRegisterAuthCodeVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="인증번호가 일치하지 않습니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_success(self, mock_cache):
        mock_cache.side_effect = lambda key: 123456 if key == "test@example.com:register:code" else None
        data = {"email": "test@example.com", "code": 123456}
        serializer = UserRegisterAuthCodeVerificationSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data


class TestPasswordUpdateEmailVerificationSerializer:

    @pytest.mark.parametrize("email", ["", None])
    def test_email_field_verification(self, email):
        data = {"email": email}

        serializer = PasswordUpdateEmailVerificationSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_not_exist_email_verification(self, mock_exists):
        mock_exists.return_value = False
        data = {"email": "test@example.com"}

        serializer = PasswordUpdateEmailVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="존재하지 않는 이메일입니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_success(self, mock_exists):
        mock_exists.return_value = True
        data = {"email": "test@example.com"}

        serializer = PasswordUpdateEmailVerificationSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data


class TestPasswordUpdateAuthCodeVerificationSerializer:

    @pytest.mark.parametrize(
        "email, code",
        [
            ("", ""),
            (None, ""),
            ("", None),
            (None, None),
        ],
    )
    def test_field_verification(self, email, code):
        data = {"email": email, "code": code}

        serializer = PasswordUpdateAuthCodeVerificationSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_email_failure(self, mock_cache):
        mock_cache.return_value = False
        data = {"email": "test@example.com", "code": 123456}
        serializer = PasswordUpdateAuthCodeVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="해당 이메일의 인증번호 요청 내역이 존재하지 않습니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_already_certified(self, mock_cache):
        mock_cache.return_value = "certified"
        data = {"email": "test@example.com", "code": 123456}
        serializer = PasswordUpdateAuthCodeVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldStateException, match="이미 인증 완료된 사용자입니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_code_mismatch(self, mock_cache):
        mock_cache.side_effect = lambda key: 123456 if key == "test@example.com:password:code" else None
        data = {"email": "test@example.com", "code": 654321}
        serializer = PasswordUpdateAuthCodeVerificationSerializer(data=data)
        with pytest.raises(InvalidFieldException, match="인증번호가 일치하지 않습니다."):
            serializer.is_valid(raise_exception=True)

    def test_validate_success(self, mock_cache):
        mock_cache.side_effect = lambda key: 123456 if key == "test@example.com:password:code" else None
        data = {"email": "test@example.com", "code": 123456}
        serializer = PasswordUpdateAuthCodeVerificationSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data


class TestCustomTokenRefreshSerializer:

    @pytest.mark.parametrize(
        "refresh",
        ["", None],
    )
    def test_field_verification(self, refresh):
        data = {"refresh": refresh}

        serializer = CustomTokenRefreshSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_refresh_token(self, mock_token_refresh_serializer_validate):
        from rest_framework_simplejwt.exceptions import TokenError

        mock_token_refresh_serializer_validate.side_effect = TokenError("Invalid token")
        data = {"refresh": "mock_invalid_refresh_token"}

        serializer = CustomTokenRefreshSerializer(data=data)
        with pytest.raises(InvalidRefreshTokenException, match="토큰이 유효하지 않습니다."):
            serializer.is_valid(raise_exception=True)
        mock_token_refresh_serializer_validate.assert_called_once()

    def test_token_reissue_success(self, mock_token_refresh_serializer_validate):
        mock_token_refresh_serializer_validate.return_value = {"access": "new_access_token"}
        data = {"refresh": "mock_valid_refresh_token"}

        serializer = CustomTokenRefreshSerializer(data=data)
        assert serializer.is_valid()
        mock_token_refresh_serializer_validate.assert_called_once()
