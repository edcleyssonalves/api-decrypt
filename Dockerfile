FROM python:3.12-slim

WORKDIR /api-decrypt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y nano

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8080