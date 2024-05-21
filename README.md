# 시작 가이드

## Requirements
해당 프로젝트는 다음 버전의 언어 및 프레임워크를 사용했습니다.

- Python 3.9.6
- Django 4.2.9
- Django REST framework 3.14.0

## Installation
```
git clone https://github.com/ROCCIA-901/roccia_901_server.git
cd roccia_901_server
```

### 가상환경 생성 및 패키지 설치
```
cd backend
python -m venv {가상환경명}
source {가상환경명}/bin/activate
pip install -r requirements.txt  
```  
<br>

### 환경변수 파일 생성

backend 디렉토리 바로 아래에 생성
- .env.dev > 개발 환경용
- .env.dev.docker > 개발 환경용(도커)
- .env.prod > 운영 환경용

```
# 환경 변수 설정

DJANGO_ENV=
DJANGO_SETTINGS_MODULE=

# 기본 설정

SECRET_KEY=
ALLOWED_HOSTS=
DEBUG=

# 데이터베이스 설정

DATABASE_HOST=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=

# Redis 설정

REDIS_URI=

# Celery 설정

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=

# 이메일 설정

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
SERVER_EMAIL=
DEFAULT_FROM_MAIL=

# 슈퍼 유저 설정

DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_USERNAME=

# cors 설정(운영 환경에서만 설정)

CORS_ALLOWED_ORIGINS=

# csrf 설정(운영 환경에서만 설정)

CSRF_TRUSTED_ORIGINS=
```

<br>

### 마이그레이션

makemigrations 명령어로 생성된 migration 파일 DB에 적용

```
python manage.py migrate
```

<br>

### 환경별 프로젝트 실행

- 개발 환경

```
cd ~/roccia_901_server/backend
python manage.py runserver
```
- 개발 환경(도커)

```
cd ~/roccia_901_server
sudo docker-compose -f docker-compose.yml up --build -d
```
- 운영 환경

```
cd ~/roccia_901_server
./deploy.sh
```
