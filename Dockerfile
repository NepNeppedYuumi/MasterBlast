FROM python:3.11.7

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements/dev.txt /app/requirements.txt
RUN pip install -r requirements.txt
