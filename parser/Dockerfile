FROM python:3.9

MAINTAINER Mikhail Mikhailov <povsedn@yandex.ru>

RUN mkdir -p /parser_app
WORKDIR /parser_app

COPY . /parser_app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "parser.py"]