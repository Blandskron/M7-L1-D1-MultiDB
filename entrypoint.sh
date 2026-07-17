#!/bin/sh
set -e

python manage.py migrate --database=default --noinput
python manage.py migrate --database=contracts --noinput
python manage.py collectstatic --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.get_or_create(username='admin', defaults={'email':'admin@example.com','is_staff':True,'is_superuser':True}); u=U.objects.get(username='admin'); u.is_staff=True; u.is_superuser=True; u.set_password('admin1234'); u.save()"
python manage.py seed_demo
exec python manage.py runserver 0.0.0.0:8000
