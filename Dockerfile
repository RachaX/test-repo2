FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.1:8080"]
LABEL authors="mirko.racic"
