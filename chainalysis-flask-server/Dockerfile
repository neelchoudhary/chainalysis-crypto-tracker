FROM python:3.7-alpine

RUN apk add --no-cache python3-dev \
    && apk add py3-pip \
    && pip install --upgrade pip

RUN apk update && apk add gcc \
    libc-dev

RUN apk add build-base


WORKDIR /chainalysis-flask-server

COPY . /chainalysis-flask-server

RUN pip3 --no-cache-dir install -r requirements.txt --ignore-installed six                                                                           

EXPOSE 8001

ENTRYPOINT [ "python3" ]
CMD [ "crypto.py" ]