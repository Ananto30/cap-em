FROM python:3.7.3-slim

COPY ./app/requirements.txt /
RUN pip3 install -r /requirements.txt

COPY ./app /app
WORKDIR /app

ENV DB_URL=postgres://capem:pass@192.168.0.107:5432/postgres

ENTRYPOINT ["/app/gunicorn_starter.sh"]