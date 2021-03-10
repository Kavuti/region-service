FROM python:3.9.2-alpine3.12 as python-alpine
RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

FROM python-alpine as python-requirements
RUN mkdir /app && cd /var/log/ && mkdir region-service
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

FROM python-requirements
ENV FLASK_APP=region_service
COPY / /app
WORKDIR /app
CMD [ "./start.sh"]