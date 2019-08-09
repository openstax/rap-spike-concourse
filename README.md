# rap-spike-concourse
Exploring Concourse-CI’s (Continuous Integration) queue resource for use in the final product of Refactor Archive.

## Table of Contents

* [Setup the development environment](#setup-the-development-environment)
  * [Requirements](#you-will-need)
  * [Clone the Git repo](#clone-the-git-repo)
  * [Run the services with Docker compose](#run-the-services-with-docker-compose)
* [Access the services](#access-services)
  * [RabbitMQ](#rabbitmq)
  * [Concourse](#concourse)
  * [PostgreSQL](#postgres)
* [S3 access for debugging](#s3-access-for-debugging)


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

#### Content Event API via FLASK

1. See events:
```
curl localhost:5000/events
```

2. Add event:
```
$ curl -d '{"ident_hash": "0889907c-f0ef-496a-bcb8-2a5bb121717f"}' -H "Content-Type: application/json" -X POST http://localhost:5000/events
```

3. See event:
```
$ curl localhost:5000/events/<id>
```

#### Postgres
Log in with psql shell to cnx-db

    make sql

### S3 access for debugging

You need opensource software [rclone][rclone] for this guide. rclone enables accessing various cloud storage providers in a way similar to rsync. It also let's you mount s3 with FUSE.

Please install it using [this guide][rcloneinstall].

#### Get your S3 credentials for accessing buckets

Login to your [aws console][awsconsole] with your credentials.

Go to upper right corner to "My Security Credentials"

![securitycredentials](https://i.imgur.com/ltnzm71.png)

Now create access keys

![accesskeys](https://i.imgur.com/zXe2dlA.png)

Copy&Paste this access keys (key id & secret access key) into your password manager or download them. You will need them later.

#### Setting up rclone

We will create a new remote location named `openstax` for accessing the Openstax sandbox buckets. If not already done [install rclone][rcloneinstall] (e.g. on Mac with `brew install rclone`).

Configure rclone with and create a new remote (n):

    rclone config

![rcloneconfig](https://i.imgur.com/jdUiGMP.png)

Name it e.g. `openstax` and choose Amazon S3:

![rclones3](https://i.imgur.com/DGGVWAw.png)








[git]: https://git-scm.com
[docker-ce]: https://docs.docker.com/install
[docker-compose]: https://docs.docker.com/compose
[docker-install]: https://docs.docker.com/compose/install
[rclone]: https://rclone.org
[rcloneinstall]: https://rclone.org/install/
[awsconsole]: https://openstax-dev-sandbox.signin.aws.amazon.com/console