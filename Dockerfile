FROM python:3.7.3-slim

WORKDIR /user/src

COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt

COPY ./app ./app
COPY ./gunicorn_starter.sh ./

ARG db_url=postgres://capem:pass@localhost:5432/postgres
ENV DB_URL=${db_url}

ENTRYPOINT ["./gunicorn_starter.sh"]