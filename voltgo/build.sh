#!/usr/bin/env bash
# exit on error
set -o errexit

cd ..

pip install -r requirements.txt

cd voltgo

python manage.py collectstatic --no-input
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin','frabartre@alum.us.es','$PASSWORD_ADMIN')" | python manage.py shell