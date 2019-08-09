FROM python:3

# - Move to the temporary workspace
WORKDIR /tmp
# - Copy the source code to an installable location
COPY ./src /tmp/src

RUN set -e \
    && pip install -r /tmp/src/requirements.txt \
    && pip install /tmp/src/ \
    && rm -rf /tmp/*

WORKDIR /

# - Provide the Concourse Resource API
RUN set -e \
    && mkdir -p /opt/resource \
    && ln -s /usr/local/bin/extractor--check /opt/resource/check \
    && ln -s /usr/local/bin/extractor--in /opt/resource/in \
    && ln -s /usr/local/bin/extractor--out /opt/resource/out
