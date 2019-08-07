# content-event-resource

## Configure Dev Environment

Change into the content-event-resource working directory

`cd ./concourse/content-event-resource`

Create a virtualenv:

`python3 -m venv .venv`

Install dependencies:

`pip install .[dev]`

### Run unit tests

`python -m pytest -vvv tests/`

### Build the docker image

`make build`

### Publish the image to dockerhub

`make publish`
