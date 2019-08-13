# content-event-resource

## Configure Dev Environment

Change into the content-event-resource working directory

`cd ./concourse/content-event-resource`

Create a virtualenv:

`python3 -m venv .venv`

Install dependencies:

`pip install .[dev]`

### Run unit tests

`make test`

### Build the docker image for development

`make build-image`

### Build the docker image tagged latest

`make tag-latest`

### Release the versioned image to dockerhub

`make release`

### Release the latest image to dockerhub

`make release-latest`
