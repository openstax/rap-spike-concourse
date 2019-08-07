FROM python:3-alpine

COPY dist/content-event-resource-*.tar.gz .
RUN pip install content-event-resource-*.tar.gz
RUN mkdir -p /opt/resource
RUN for script in check in out; do ln -s $(which $script) /opt/resource/; done
