FROM python:3.10.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /rates-task

WORKDIR /rates-task

COPY . /rates-task

RUN pip install -r requirements.txt
