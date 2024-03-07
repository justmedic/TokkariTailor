FROM python:3.12.0

WORKDIR /backend

COPY backend/requirements.txt /backend/

RUN pip install -r requirements.txt

COPY backend/ /backend/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
