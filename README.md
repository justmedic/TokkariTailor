
Скопировать
```
git clone https://github.com/justmedic/TokkariTailor
```

Войти в директорию
```
cd Tokkaritailor
```

Обязательно нужно сделать миграции (по отдельности потому что оно работрает с помощью древних шизобогов)
```
python manage.py makemigrations shop
python manage.py makemigrations home
python manage.py makemigrations cart
python manage.py makemigrations accounts

python manage.py migrate
```

Докер
```
docker-compose up --build
```

Сайт
```
http://localhost:8000/
```
