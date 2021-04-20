web: daphne tests.asgi:application --port $PORT --bind 0.0.0.0

celery-bg: celery -A celery_app worker -l info -Ofair --concurrency=1 -E

release: python manage.py migrate