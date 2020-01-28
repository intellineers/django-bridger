docker-compose up -d 
git pull 
python manage.py migrate 
python manage.py runserver 0.0.0.0:5000