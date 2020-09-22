FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code/

ENV DB_NAME=myphotos
ENV DB_HOST=127.0.0.1
ENV DB_PORT=27017
ENV BASIC_AUTH_USERNAME=admin
ENV BASIC_AUTH_PASSWORD=Qbubigf12345


CMD uwsgi --http 0.0.0.0:5000 wsgi.ini