FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl

WORKDIR /home/app/web

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

FROM base AS black

RUN pip install black

RUN black --check .

FROM black AS pylint

ENV DJANGO_SETTINGS_MODULE=config.settings

RUN pip install pylint pylint-django[with-django]

RUN pylint --load-plugins pylint_django .

FROM pylint AS unittest

RUN pip install pytest-django

RUN python3 manage.py makemigrations --settings=config.unittest --noinput

RUN python3 manage.py migrate --settings=config.unittest --noinput

RUN DJANGO_SETTINGS_MODULE=config.unittest pytest

FROM unittest AS sast

RUN pip install bandit

RUN bandit -r . || exit 1

FROM base AS build

RUN chmod +x entrypoint.sh

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "./entrypoint.sh"]
