release: pip install -r requirements.txt --no-dependencies
release: python manage.py migrate
web: python manage.py runserver 0.0.0.0:$PORT
