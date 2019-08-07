# rap-spike-concourse
Exploring Concourse-CI’s (Continuous Integration) queue resource for use in the final product of Refactor Archive.

## Table of Contents

* [Setup the development environment](#creating-the-spike-concourse-development-environment)
  * [Requirements](#you-will-need)
  * [Clone the Git repo](#clone-the-git-repo)
  * [Run the services with Docker compose](#run-the-services-with-docker-compose)
* [Access the services](#access-services)
  * [RabbitMQ](#rabbitmq)
  * [Concourse](#concourse)
  * [PostgreSQL](#postgres)


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

To stop any of the docker containers, obtain the CONTAINER ID by running `docker container ls`, then:

    docker stop [CONTAINER ID]

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

#### Postgres
Log in with psql shell to cnx-db

    make sql

[git]: https://git-scm.com
[docker-ce]: https://docs.docker.com/install
[docker-compose]: https://docs.docker.com/compose
[docker-install]: https://docs.docker.com/compose/install
