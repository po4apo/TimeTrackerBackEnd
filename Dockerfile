FROM python:3.11.1
LABEL authors="main"

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y install netcat

COPY . /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENTRYPOINT ["/usr/src/app/entrypoint.sh"]