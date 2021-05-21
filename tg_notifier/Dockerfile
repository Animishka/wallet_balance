FROM python:3.9

MAINTAINER Mikhail Mikhailov <povsedn@yandex.ru>

RUN mkdir -p /tg_notifier_app
WORKDIR /tg_notifier_app
COPY . /tg_notifier_app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "tg_notifier.py"]