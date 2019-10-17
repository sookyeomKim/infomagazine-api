FROM python:3.7
MAINTAINER skkim <ikks06luck@gmail.com>

COPY ./Pipfile /home
COPY ./Pipfile.lock /home
COPY ./backend /home/api
COPY ./docker/prod /home/docker

WORKDIR /home

RUN pip install --upgrade pip

RUN pip install pipenv

RUN pipenv install --system

RUN apt-get update && apt-get install -y uwsgi-plugin-python3 \
    && apt-get install -y uwsgi-plugin-python && apt-get install -y vim \
    && apt-get install -y git

RUN pip install uwsgi && pip install git+https://github.com/Supervisor/supervisor

RUN chmod +x /home/docker/config/run.sh

CMD /home/docker/config/run.sh