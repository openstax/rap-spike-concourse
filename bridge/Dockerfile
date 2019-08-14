FROM python:3

WORKDIR /
# - Copy the source code to an installable location
COPY ./src /tmp/src
COPY ./tasks /tasks

RUN set -e \
    && pip install -r /tmp/src/requirements.txt \
    && pip install /tmp/src \
    && rm -rf /tmp/*
