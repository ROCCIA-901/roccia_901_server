from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('사용자는 이메일을 가지고 있어야 합니다.')
        if 'username' not in extra_fields or not extra_fields['username']:
            raise ValueError('사용자는 사용자명을 가지고 있어야 합니다.')
        if 'generation' not in extra_fields or not extra_fields['generation']:
            raise ValueError('사용자는 세대를 가지고 있어야 합니다.')
        if 'role' not in extra_fields or not extra_fields['role']:
            raise ValueError('사용자는 역할을 가지고 있어야 합니다.')
        if 'workout_location' not in extra_fields or not extra_fields['workout_location']:
            raise ValueError('사용자는 운동 위치를 가지고 있어야 합니다.')
        if 'workout_level' not in extra_fields or not extra_fields['workout_level']:
            raise ValueError('사용자는 운동 레벨을 가지고 있어야 합니다.')
        if 'profile_number' not in extra_fields or not extra_fields['profile_number']:
            raise ValueError('사용자는 프로필 번호를 가지고 있어야 합니다.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        if extra_fields.get('role') == 'manager':
            user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('manager', '운영진'),
        ('member', '부원'),
    )

    WORKOUT_LOCATION_CHOICES = (
        ('일산', '일산'),
        ('연남', '연남'),
        ('양재', '양재'),
        ('신림', '신림'),
    )

    WORKOUT_LEVEL = (
        ('white', '하얀색'),
        ('yellow', '노란색'),
        ('orange', '주황색'),
        ('green', '초록색'),
        ('blue', '파란색'),
        ('red', '빨간색'),
        ('purple', '보라색'),
        ('grey', '회색'),
        ('brown', '갈색'),
        ('black', '검정색'),
    )

    email = models.EmailField(max_length=30, unique=True, null=False, blank=False, help_text='이메일')
    password = models.CharField(max_length=20, help_text='비밀번호')
    username = models.CharField(max_length=20, help_text='사용자 이름')
    generation = models.IntegerField(help_text='기수')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='manager', help_text='역할')
    workout_location = models.CharField(max_length=100, choices=WORKOUT_LOCATION_CHOICES, help_text='운동 지점')
    workout_level = models.CharField(max_length=100, choices=WORKOUT_LEVEL, help_text='운동 난이도')
    profile_number = models.IntegerField(help_text='프로필 번호')
    introduction = models.TextField(help_text='소개글')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성 일시')
    updated_at = models.DateTimeField(auto_now=True, help_text='수정 일시')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
