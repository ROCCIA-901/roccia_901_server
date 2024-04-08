import os
from datetime import timedelta

import environ

from .base import *


def load_env_settings():
    if django_env == "dev.docker":
        env_file = os.path.join(BASE_DIR, ".env.dev.docker")
    else:
        env_file = os.path.join(BASE_DIR, ".env.dev")

    env_settings = environ.Env()
    if os.path.isfile(env_file):
        environ.Env.read_env(env_file=env_file)
    return env_settings


# 필수 설정

django_env = os.getenv("DJANGO_ENV", "dev")
env = load_env_settings()
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# 데이터베이스 설정

POSTGRES_DB = env("POSTGRES_DB", default="")
if POSTGRES_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": env("POSTGRES_USER", default=""),
            "PASSWORD": env("POSTGRES_PASSWORD", default=""),
            "HOST": env("POSTGRES_HOST", default=""),
            "PORT": env("POSTGRES_PORT", default=""),
            "OPTIONS": {"options": "-c timezone=Asia/Seoul"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# JWT 설정

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# smtp 설정

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
SERVER_EMAIL = env("SERVER_EMAIL", default="")
DEFAULT_FROM_MAIL = env("DEFAULT_FROM_MAIL", default="")

# 정적 파일 설정

if django_env == "dev.docker":
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
