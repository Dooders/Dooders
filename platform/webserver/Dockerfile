FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip

RUN pip3 install Flask gunicorn
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
WORKDIR /app
COPY . /app