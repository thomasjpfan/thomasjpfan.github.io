FROM python:3.6.4-alpine3.7

WORKDIR /blog
COPY requirements.txt .

RUN apk add --update --no-cache --virtual build-deps \
    build-base libffi-dev ruby-dev \
    jpeg-dev zlib-dev gcc libc-dev musl-dev && \
    apk add --no-cache ruby make libjpeg optipng libjpeg-turbo-utils && \
    gem install sass compass --no-ri --no-rdoc && \
    pip install -r requirements.txt && \
    apk del build-deps && \
    rm -rf /root/.cache/pip/* && \
    rm -rf /var/cache/apk/*

ENTRYPOINT [ "" ]
