FROM python:3.12.0

WORKDIR /backend

COPY backend/requirements.txt /backend/

RUN pip install -r requirements.txt
COPY backend/ /backend/
COPY init.sh /backend/  
RUN chmod +x /backend/init.sh

ENTRYPOINT ["/backend/init.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
