FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./uvicorn_starter.sh .
RUN chmod +x uvicorn_starter.sh

ENTRYPOINT ["./uvicorn_starter.sh"]