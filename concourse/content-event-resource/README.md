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


## Concourse Interface

This Concourse Resource is used for checking and acquiring events from the event service application.

## Source Configuration

* `api_root`: URL to the events service API root (e.g. `http://content-events-api:5000`)
* `status`: indicates which status this resource should become active for (e.g. `queued`)

## Behavior

### `check`: Produce timestamps satisfying the interval.

Checks for new events

### `in`: Report the given time.

Pulls in the versioned event for processing.

Writes the following files to output:

- `id`: contains the event id
- `ident_hash`: contains the ident-hash for the event
- `event.json`: a copy of the event data

#### Parameters

*None.*

### `out`: Produce the current time.

Not implemented

#### Parameters

*None.*
