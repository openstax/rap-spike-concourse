FROM python:3

# We could really use some kind of debian dockerfile instructions wrapper script Something like `capt install libxml2`.

# - Install the system dependencies
RUN apt-get update \
    && apt-get install \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

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
