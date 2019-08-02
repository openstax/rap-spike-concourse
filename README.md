# rap-concourse-spike

## Creating the concourse spike development environment

### You will need

* [Git][git]
* [Docker CE][docker-ce] and [Docker Compose][docker-compose]  
  Follow the [instructions on the docker website][docker-install] to install these.

### Clone the Git repo

    git clone git@github.com:openstax/rap-concourse-spike.git

This will download the code into a `rap-concourse-spike` directory. You will need to be in  the `rap-concourse-spike` directory for the remainder of the installation process.

    cd rap-concourse-spike

### Run the services with Docker Compose

Start the services that are required with Docker Compose:

    make services

You'll now have some Docker containers running the PostgreSQL databases for cnx-db and Concourse, the Concourse application, and RabbitMQ. You should be able to see all the services by running:

    docker-compose ps

### Logging into Concourse

With your browser visit `http://localhost:8080`

Enter the following to login 

```
username: test
password: test
```

### Logging in with psql shell to cnx-db

    make sql

[git]: https://git-scm.com
[docker-ce]: https://docs.docker.com/install
[docker-compose]: https://docs.docker.com/compose
[docker-install]: https://docs.docker.com/compose/install

