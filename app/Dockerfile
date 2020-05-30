FROM python:3.7.3-slim

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENV DB_URL=postgres://capem:pass@192.168.0.107:5432/postgres

RUN chmod +x /app/gunicorn_starter.sh

ENTRYPOINT ["/app/gunicorn_starter.sh"]