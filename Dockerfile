FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./app ./app
COPY ./gunicorn_starter.sh ./

ENTRYPOINT ["./gunicorn_starter.sh"]