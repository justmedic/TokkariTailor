#!/bin/bash
set -e

echo "Выполнение миграций для приложений..."

python manage.py makemigrations shop
python manage.py makemigrations home
python manage.py makemigrations cart
python manage.py makemigrations accounts

echo "Применение миграций..."

python manage.py migrate --noinput

echo "Создание суперпользователя admin..."

echo "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    User.objects.create_superuser('admin', 'admin@example.com', '12345678')
    print('Суперпользователь создан.')
except Exception as e:
    print('Ошибка при создании суперпользователя:', str(e))
" | python manage.py shell

echo "Запуск сервера..."
python manage.py runserver 0.0.0.0:8000
