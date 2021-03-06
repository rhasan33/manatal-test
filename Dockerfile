FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir src

RUN apt-get update && apt-get install build-essential curl -y && \
    pip3 install -U pip

RUN pip3 install pipenv

ADD Pipfile* /tmp

ADD wait-for-it.sh /app
RUN chmod +x wait-for-it.sh

RUN cd /tmp && pipenv lock -d --requirements > requirements.txt \
    && pip install -r /tmp/requirements.txt

COPY src/ /app/src/

EXPOSE 8000
