# rap-spike-concourse
Exploring Concourse-CI’s (Continuous Integration) queue resource for use in the final product of Refactor Archive.

## Table of Contents

* [Setup the development environment](#setup-the-development-environment)
  * [Requirements](#you-will-need)
  * [Clone the Git repo](#clone-the-git-repo)
  * [Setup S3 before running Docker Compose](#setup-s3-before-running-docker-compose)
  * [Run the services with Docker compose](#run-the-services-with-docker-compose)
  * [Initialize DB on first run](#initialize-db-on-first-run)
* [Access the services](#access-services)
  * [RabbitMQ](#rabbitmq)
  * [Concourse](#concourse)
  * [Content Event API](#content-event-api-via-flask)
  * [PostgreSQL](#postgres)
* [S3 access for debugging](#s3-access-for-debugging)
  * [Get your S3 credentials](#get-your-s3-credentials)
  * [Setting up rclone](#setting-up-rclone)
  * [Test that rclone works](#test-that-rclone-works)
  * [How to use rclone](#how-to-use-rclone)
  * [How to mount a bucket into your local filesystem with FUSE](#how-to-mount-a-bucket-into-your-local-filesystem-with-fuse)
  * [Mac and Cyberduck](#mac-and-cyberduck)
* [Concourse](#concourse)
  * [`fly` commands](#fly-commands)
    * [Create a target](#create-a-target)
    * [Add a pipeline](#add-a-pipeline)
  * [Pipelines](#pipelines)
  * [Content event resource](#content-event-resource)
* [End Result](#end-result)

## A3 Problem Solving

### Background (PLAN)

This spike is an experiment in itself to test the viability of using the Concourse CI system to react
to publishing events from cnx-db and conduct work using the concept of a pipeline. The work
primarily consists of extracting content from the database and uploading it to Amazon S3.

This spike's main purpose is if we can utilize Concourse to this end.

### Current condition (PLAN)

In the current system CMs, Baking, and consumers all rely on the same database.

![image](https://user-images.githubusercontent.com/8730430/64211160-e841ea80-ce6a-11e9-9452-8c03ad7a0ff3.png)

### Goal / Target Condition (PLAN)

Create the "one-way" bridge as a concourse pipeline that can react to events and extract content/resources from the database and upload to S3.

![image](https://user-images.githubusercontent.com/8730430/64211419-ba10da80-ce6b-11e9-9537-f683f97b13ed.png)

### Root Cause Analysis (PLAN)


### Countermeasures (DO)

### Confirmation (CHECK)

### Follow up (ACT)

## Setup the development environment

### You will need

* [Git][git]
* [Docker CE][docker-ce] and [Docker Compose][docker-compose]  
  Follow the [instructions on the docker website][docker-install] to install these.

### Clone the Git repo

    git clone git@github.com:openstax/rap-spike-concourse.git

This will download the code into a `rap-spike-concourse` directory. You will need to be in  the `rap-spike-concourse` directory for the remainder of the installation process.

    cd rap-spike-concourse

### Setup S3 before running Docker Compose

Get your S3 credentials according to this [chapter](#s3-access-for-debugging) and insert your credentials in a file named

```
credentials.yml
```

the file should content should look like this:

```yml
aws-access-key: samplekey
aws-secret-key: samplesecret
s3bucket: ce-rap-test
s3region: us-east-2
```


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
curl -d '{"ident_hash": "4b5aaf32-1de1-419b-bdc0-4e0a7f6daf0f@27", "status": "queued"}' -H "Content-Type: application/json" -X POST http://localhost:5000/events
```

3. See event:
```
$ curl localhost:5000/events/<id>
```

### Postgres
Log in with psql shell to cnx-db

    make sql

### S3 access for debugging

You need opensource software [rclone][rclone] for this guide. rclone enables accessing various cloud storage providers in a way similar to rsync. It also let's you mount s3 with FUSE.

Please install it using [this guide][rcloneinstall].

Info for Mac users:

* Install [FUSE for macOS][macosfuse] first.
* You can install rclone easily with `brew install rclone`.

#### Get your S3 credentials

Login to your [aws console][awsconsole] with your credentials.

Go to upper right corner to "My Security Credentials"

![securitycredentials](https://user-images.githubusercontent.com/1050582/62883460-c27a6780-bd3c-11e9-9982-7469b6f8408c.jpg)

Now create access keys

![accesskeys](https://user-images.githubusercontent.com/1050582/62883461-c27a6780-bd3c-11e9-8770-68650ddba263.jpg)

Copy&Paste this access keys (key id & secret access key) into your password manager or download them. You will need them later.

#### Setting up rclone

We will create a new remote location named `openstax` for accessing the Openstax sandbox buckets. If not already done [install rclone][rcloneinstall] (e.g. on Mac with `brew install rclone`).

* Configure rclone with and create a new remote (n):

```
rclone config
```

![rcloneconfig](https://user-images.githubusercontent.com/1050582/62883463-c27a6780-bd3c-11e9-83f3-21bc0a037cbd.jpg)

* Name it e.g. `openstax` and choose Amazon S3:

![rclones3](https://user-images.githubusercontent.com/1050582/62883464-c312fe00-bd3c-11e9-9d90-404bde984996.jpg)

* Choose S3
* Enter AWS credentials in next step
* Now enter your access key id and secret access key inside:

![rclonesecret](https://user-images.githubusercontent.com/1050582/62883465-c312fe00-bd3c-11e9-94aa-eaba436bd5b7.jpg)

* Choose Ohio: `us-east-2`
* Use default entpoint
* Choose again Ohio: `us-east-2`
* Choose FULL_CONTROL for owner (default):

![rclonefullcontrol](https://user-images.githubusercontent.com/1050582/62883466-c312fe00-bd3c-11e9-8c12-b7ee4c68c7fd.jpg)

* Choose no server side encryption
* No KMS ID:

![rclonekms](https://user-images.githubusercontent.com/1050582/62883467-c312fe00-bd3c-11e9-97f7-6c0947e16aa6.jpg)

* Default storage class
* No advanced config

* At the end confirm all your settings which should look similar to this:

![rcloneconfirm](https://user-images.githubusercontent.com/1050582/62883469-c3ab9480-bd3c-11e9-819c-59c2d222adea.jpg)

* quit config

#### Test that rclone works

Run following command to remote `openstax` look at the buckets available:

```
rclone lsd openstax:
```

You should see a list of buckets and also our test bucket `ce-rap-test`:

![ce-rap-test](https://user-images.githubusercontent.com/1050582/62883470-c3ab9480-bd3c-11e9-9c7a-c77b171a0185.jpg)

#### How to use rclone

Some examples of rclone usage.

List the contents of bucket `ce-rap-test`:

```
rclone ls openstax:ce-rap-test
```

Copy all content from `ce-rap-test` to your current directory:

```
rclone copy openstax:ce-rap-test ./
```

Copy one file into the bucket:

```
rclone copy ./nothinginside.md openstax:ce-rap-test/
```

Information: Be careful with `move` and `delete` commands!

#### How to mount a bucket into your local filesystem with FUSE

rclone can also mount buckets into your local filesystem with FUSE.

Info: On mac you need to install [FUSE for macOS][macosfuse] first.

First create a local folder e.g. in your home dir where you want to mount the bucket. For example:

```
mkdir ~/s3files
```

Now mount the bucket with rclone in the foreground:

```
rclone mount openstax:ce-rap-test ~/s3files
```

or if you want to mount the bucket in the background you just need to add a `&` in the command:
```
rclone mount openstax:ce-rap-test ~/s3files &
```

**Now you can use that folder as remote mount and can copy/move/delete files into s3 and out!**

To stop mounting from foreground mount press `Ctrl-C`. Sometimes unmounting can fail. In this case use this command to unmount your mount folder manually:

```bash
# Linux
fusermount -u /s3files
# OS X
umount /s3files
```

#### Mac and Cyberduck

On macOS there is a very easy to use UI interface for accessing S3 buckets and also for managing user rights in S3 buckets.

It's free and easy to use: [CyberDuck][cyberduck]

I don't write a specific guide for Cyberduck because it is self explanatory and works quite similar to FTP programs.

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

#### Test S3 pipeline with dummy data

    fly -t dev set-pipeline -p test-s3-dummy -c concourse/test-s3-dummydata.yml -l credentials.yml

### Pipelines

Pipelines for this repository are contained in the [concourse](./concourse) folder.

### Content event resource

Access the [README.md](./concourse/content-event-resource/README.md) in the content event resource directory.

If you are doing development for the resource it's helpful to change into the directory.

[git]: https://git-scm.com
[docker-ce]: https://docs.docker.com/install
[docker-compose]: https://docs.docker.com/compose
[docker-install]: https://docs.docker.com/compose/install
[rclone]: https://rclone.org
[rcloneinstall]: https://rclone.org/install/
[awsconsole]: https://openstax-dev-sandbox.signin.aws.amazon.com/console
[macosfuse]: https://osxfuse.github.io/
[cyberduck]: https://cyberduck.io/

## End Result

The end result of all this is an implementation of what could constitute the Bridge section of Refactor Archive. We don't use a live database with publications in this, but our use of `curl` to introduce an event (aka publication) into the system is a sufficient abstraction.

1. First of all, set up an S3 bucket for yourself using the instructions in this document.
1. `cp credentials.yml.template credentials.yml`
1. Edit `credentials.yml` to include your S3 bucket information
1. Make sure you're `fly` client is logged into concourse (we use the `-t dev` target option in these examples)
1. `fly -t dev sp -p bridge -c concourse/bridge.yml -l credentials.yml`
1. Create an event: `curl -d '{"ident_hash": "4b5aaf32-1de1-419b-bdc0-4e0a7f6daf0f@27", "status": "queued"}' -H "Content-Type: application/json" -X POST http://localhost:5000/events`
1. Trigger the job and watch the output: `fly -t dev tj -j bridge/pulling-content-into-s3 -w`

The last step isn't absolutely necessary since the pipeline is setup to watch for events. But doing this last step allows us to see the situation in a controlled way.
