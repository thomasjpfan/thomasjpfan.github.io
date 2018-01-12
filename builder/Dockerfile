FROM python:3.6.4-alpine3.7

RUN apk add --no-cache ruby make libjpeg optipng libjpeg-turbo-utils && \
    apk add --no-cache --virtual build-deps \
    build-base libffi-dev ruby-dev && \
    gem install sass compass --no-ri --no-rdoc && \
    apk del build-deps

WORKDIR /blog
COPY requirements.txt .

RUN apk add --no-cache --virtual build-deps \
    jpeg-dev zlib-dev build-base && \
    pip install -r requirements.txt && \
    apk del build-deps && \
    rm -rf /root/.cache/pip/*

ENTRYPOINT [ "" ]
