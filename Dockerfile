FROM python:3.7.3-slim

COPY ./app/requirements.txt /
RUN pip3 install -r /requirements.txt

COPY ./app /app
WORKDIR /app

ARG db_url=postgres://capem:pass@localhost:5432/postgres
ENV DB_URL=${db_url}

ENTRYPOINT ["/app/gunicorn_starter.sh"]