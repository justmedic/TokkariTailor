FROM python:3.12.0

WORKDIR /backend

COPY backend/requirements.txt /backend/

RUN pip install -r requirements.txt

COPY backend/ /backend/

RUN chmod +x init.sh
ENTRYPOINT ["./init.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
