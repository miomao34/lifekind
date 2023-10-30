FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt makefile main.py ./
COPY assets assets

RUN apk add make
RUN make setup

CMD ["make", "run-docker"]