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

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '12345678')" | python manage.py shell



echo "Запуск сервера..."

