flask db upgrade
gunicorn -w 4 --bind=0.0.0.0 wsgi:app