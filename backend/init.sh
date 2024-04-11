python manage.py migrate --no-input
python manage.py initadmin
python manage.py collectstatic --no-input
gunicorn --config gunicorn.conf.py config.wsgi:application
python manage.py runapscheduler
