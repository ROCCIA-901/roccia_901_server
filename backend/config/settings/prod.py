from datetime import timedelta

import environ

from .base import *

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env.prod")
environ.Env.read_env(env_file=env_file)

# 필수 설정

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# 데이터베이스 설정

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": env("DATABASE_HOST", default=""),
        "PORT": env("DATABASE_PORT", default=""),
        "NAME": env("DATABASE_NAME", default=""),
        "USER": env("DATABASE_USER", default=""),
        "PASSWORD": env("DATABASE_PASSWORD", default=""),
    }
}

# Redis 설정

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URI", default=""),
        "OPTION": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
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

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
