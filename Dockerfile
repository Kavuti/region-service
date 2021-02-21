FROM python:3.9.1-alpine3.12 as python-alpine
RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

FROM python-alpine as python-requirements
RUN mkdir /app && cd /var/log/ && mkdir region-service
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

FROM python-requirements
COPY / /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=region_service

ENTRYPOINT [ "gunicorn", "-w 4", "--bind=0.0.0.0", "wsgi:app" ]