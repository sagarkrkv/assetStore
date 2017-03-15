FROM python:3.5.3-alpine

RUN apk add --no-cache  gcc python3-dev musl linux-headers build-base


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r /app/requirements.txt


COPY . /app

EXPOSE 8080

CMD ["python3", "-m","swagger_server"]
