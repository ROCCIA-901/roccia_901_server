# Django 관련 명령 실행
python manage.py migrate --no-input
python manage.py initadmin
python manage.py collectstatic --no-input

# gunicorn 웹 서버 실행
gunicorn --config gunicorn.conf.py config.wsgi:application &

# APScheduler 실행
#python manage.py runapscheduler &
python manage.py runapscheduler --minutes=1 &

# Celery 실행 -> 컨테이너 실행으로 변경
#celery -A config worker --loglevel=info &

# 모든 백그라운드 작업이 완료될 때까지 기다림
wait
