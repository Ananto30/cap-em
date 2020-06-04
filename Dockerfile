FROM python:3.7.3-slim

WORKDIR /user/src

COPY ./requirements.txt ./
RUN pip3 install -r ./requirements.txt

COPY ./app ./app
COPY ./gunicorn_starter.sh ./

ENTRYPOINT ["./gunicorn_starter.sh"]