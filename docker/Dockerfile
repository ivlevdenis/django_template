FROM python:3.7-alpine

RUN apk add --update build-base ca-certificates make
RUN apk add  --no-cache \
    libjpeg \
    zlib \
    zlib-dev \
    libwebp \
    openjpeg \
    jpeg-dev \
    postgresql-libs \
    postgresql-dev \
    ncurses-dev \
    readline-dev \
    bash

WORKDIR /app
COPY /project/requirements.txt /project/Makefile /app/
COPY /project/requirements /app/requirements/
RUN make req-dev

EXPOSE 8000