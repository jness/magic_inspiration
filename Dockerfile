FROM python:3.6
ENV PYTHONUNBUFFERED 1

ADD . /magic_inspiration
WORKDIR /magic_inspiration

RUN pip install -r requirements.txt
