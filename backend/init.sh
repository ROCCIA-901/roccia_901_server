python manage.py migrate --no-input
python manage.py initadmin
python manage.py collectstatic --no-input
python manage.py runapscheduler.py
gunicorn --config gunicorn.conf.py config.wsgi:application
