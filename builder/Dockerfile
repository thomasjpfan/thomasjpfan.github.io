FROM python:3.6.4-alpine3.7

WORKDIR /blog
COPY requirements.txt .

RUN apk add --no-cache make libjpeg optipng \
    libjpeg-turbo-utils libstdc++ && \
    apk add --no-cache --virtual build-deps \
    jpeg-dev zlib-dev build-base && \
    pip install -r requirements.txt && \
    apk del build-deps && \
    rm -rf /root/.cache/pip/*

ENTRYPOINT [ "" ]
