FROM nginx:latest
MAINTAINER skkim <ikks06luck@gmail.com>

COPY ./docker/prod /home/docker

WORKDIR /home

RUN rm /etc/nginx/conf.d/default.conf

COPY docker/prod/config/default.conf /etc/nginx/conf.d/default.conf
COPY docker/prod/config/nginx.conf /etc/nginx/nginx.conf