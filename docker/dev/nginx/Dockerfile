FROM nginx:latest
MAINTAINER skkim <ikks06luck@gmail.com>

COPY ./docker/dev /home/docker

WORKDIR /home

RUN rm /etc/nginx/conf.d/default.conf

COPY docker/dev/config/nginx.conf /etc/nginx/conf.d/default.conf