web: python manage.py runserver 0.0.0.0:5000

celery-bg: celery -A celery_app worker -l info -Ofair --concurrency=1 -E

release: python manage.py migrate