#!/bin/sh
echo "Starting migrate"
python manage.py migrate
echo "Creating superuser"
python manage.py create_local_superuser
echo "Starting runserver"
python manage.py runserver 0.0.0.0:8000