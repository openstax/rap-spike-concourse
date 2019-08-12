# rap-spike-concourse
Exploring Concourse-CI’s (Continuous Integration) queue resource for use in the final product of Refactor Archive.

## Table of Contents

* [Setup the development environment](#creating-the-spike-concourse-development-environment)
  * [Requirements](#you-will-need)
  * [Clone the Git repo](#clone-the-git-repo)
  * [Run the services with Docker compose](#run-the-services-with-docker-compose)
  * [Initialize DB on first run](#initialize-db-on-first-run)
* [Access the services](#access-services)
  * [RabbitMQ](#rabbitmq)
  * [Concourse](#concourse)
  * [Content Event API](#content-event-api-via-flask)
  * [PostgreSQL](#postgres)
* [Concourse](#concourse)
  * [`fly` commands](#fly-commands)
    * [Create a target](#create-a-target)
    * [Add a pipeline](#add-a-pipeline)
  * [Pipelines](#pipelines)
  * [Content event resource](#content-event-resource)


## Setup the development environment

### You will need

* [Git][git]
* [Docker CE][docker-ce] and [Docker Compose][docker-compose]  
  Follow the [instructions on the docker website][docker-install] to install these.

### Clone the Git repo

    git clone git@github.com:openstax/rap-spike-concourse.git

This will download the code into a `rap-spike-concourse` directory. You will need to be in  the `rap-spike-concourse` directory for the remainder of the installation process.

    cd rap-spike-concourse

### Run the services with Docker Compose

Start the services that are required with Docker Compose:

    make services

You'll now have four Docker containers running the PostgreSQL databases for cnx-db and Concourse, the Concourse application, and RabbitMQ. You should be able to see all the services by running:

    docker-compose ps

To stop any of the docker containers:

    docker-compose stop [SERVICE...]  # e.g. docker-compose stop cnx-db

### Initialize DB on first run

On first run the DB needs to be recreated from the DB dump:

    make initdb

This reinitializes the DB (drops, recreates DB and restores DB dump) with this three books:

* Elementary Algebra (col12116), id `0889907c-f0ef-496a-bcb8-2a5bb121717f`
* Intermediate Algebra (col12119), id `02776133-d49d-49cb-bfaa-67c7f61b25a1`
* Prealgebra (col11756), id `caa57dab-41c7-455e-bd6f-f443cda5519c`

## Access Services

Access the services that have been started by Docker Compose.

- Concourse-CI (HTTP): http://localhost:8080
- RabbitMQ (AMQP): amqp://guest:guest@localhost:5672
- RabbitMQ Management (HTTP): http://guest:guest@localhost:15672
- Postgres: postgres://rhaptos@localhost:15432/repository

### RabbitMQ

Log into RabbitMQ with your browser, visit `http://localhost:15672`

Enter the following to login

```
username: guest
password: guest
```

### Concourse

Log into Concourse with your browser, visit `http://localhost:8080`

Enter the following to login

```
username: test
password: test
```

### Content Event API via FLASK

1. See events:
```
curl localhost:5000/events
```

2. Add event:
```
curl -d '{"ident_hash": "0889907c-f0ef-496a-bcb8-2a5bb121717f", "status": "queued"}' -H "Content-Type: application/json" -X POST http://localhost:5000/events
```

3. See event:
```
$ curl localhost:5000/events/<id>
```

### Postgres
Log in with psql shell to cnx-db

    make sql

## Concourse

### `fly` commands

In order to use of pipelines you must first create a target for your Concourse instance.

#### Create a target

    fly --target dev login --concourse-url http://0.0.0.0:8080 -u test -p test

You will need to unpause a newly created pipeline. The output for the command
will provide you with options.

#### Add a pipeline

    fly -t dev set-pipeline -p publish-pipeline -c concourse/show-queued-pipeline.yml

To update a pipeline you can use the same command to add a pipeline. You will be
shown a diff of the server held pipeline and your changes.

### Pipelines

Pipelines for this repository are contained in the [concourse](./concourse) folder.

### Content event resource

Access the [README.md](./concourse/content-event-resource/README.md) in the content event resource directory.

If you are doing development for the resource it's helpful to change into the directory.

[git]: https://git-scm.com
[docker-ce]: https://docs.docker.com/install
[docker-compose]: https://docs.docker.com/compose
[docker-install]: https://docs.docker.com/compose/install
