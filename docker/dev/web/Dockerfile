FROM python:3.7
MAINTAINER skkim <ikks06luck@gmail.com>

COPY ./Pipfile /home
COPY ./Pipfile.lock /home
COPY ./docker/dev /home/docker

WORKDIR /home

RUN pip install --upgrade pip

RUN pip install pipenv

RUN pipenv install --system --dev

RUN apt-get update && apt-get install -y uwsgi-plugin-python3 \
    && apt-get install -y uwsgi-plugin-python && apt-get install -y vim \
    && apt-get install -y git

RUN pip install uwsgi && pip install git+https://github.com/Supervisor/supervisor

CMD docker/config/run.sh