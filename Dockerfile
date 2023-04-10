FROM python:3.10-slim

WORKDIR /

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]