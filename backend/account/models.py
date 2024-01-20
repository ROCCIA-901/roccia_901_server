from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('사용자는 이메일을 가지고 있어야 합니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        if extra_fields.get('role') == '운영진':
            user.is_staff = True

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼 유저의 is_staff 필드는 True여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼 유저의 is_superuser 필드는 True여야 합니다.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('운영진', '운영진'),
        ('부원', '부원'),
    )

    WORKOUT_LOCATION_CHOICES = (
        ('일산', '일산'),
        ('연남', '연남'),
        ('양재', '양재'),
        ('신림', '신림'),
    )

    WORKOUT_LEVELS = (
        ('하얀색', '하얀색'),
        ('노란색', '노란색'),
        ('주황색', '주황색'),
        ('초록색', '초록색'),
        ('파란색', '파란색'),
        ('빨간색', '빨간색'),
        ('보라색', '보라색'),
        ('회색', '회색'),
        ('갈색', '갈색'),
        ('검정색', '검정색'),
    )

    GENERATION_CHOICES = (
        ('1기', '1기'),
        ('2기', '2기'),
        ('3기', '3기'),
        ('4기', '4기'),
        ('5기', '5기'),
        ('6기', '6기'),
        ('7기', '7기'),
        ('8기', '8기'),
        ('9기', '9기'),
        ('10기', '10기'),
        ('11기', '11기'),
    )

    email = models.EmailField(max_length=30, unique=True, null=False, blank=False, help_text='이메일')
    username = models.CharField(max_length=20, help_text='사용자 이름')
    generation = models.CharField(max_length=10, help_text='기수', choices=GENERATION_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='부원', help_text='역할')
    workout_location = models.CharField(max_length=100, choices=WORKOUT_LOCATION_CHOICES, help_text='운동 지점')
    workout_level = models.CharField(max_length=100, choices=WORKOUT_LEVELS, help_text='운동 난이도')
    profile_number = models.IntegerField(help_text='프로필 번호')
    introduction = models.TextField(max_length=500, help_text='소개글')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성 일시')
    updated_at = models.DateTimeField(auto_now=True, help_text='수정 일시')

    is_active = models.BooleanField(default=True, help_text='활성 상태')
    is_staff = models.BooleanField(default=False, help_text='스태프 상태')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
