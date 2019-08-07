.PHONY: default
default: help

.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make services          Run the services that Concourse and the pipeline requires"
	@echo "make sql               Connect to the cnx-db database with a psql shell"

.PHONY: services
services:
ifneq ("$(wildcard ./20190805_dump.sql.gz)","")
	docker-compose up -d
else
	@echo Downloading db dump file first...
	rsync -tv --progress -e 'ssh -T -c aes128-ctr -o Compression=no -x' backup1.cnx.org:/var/backups/db_dump/20190805_dump.sql.gz ./
	docker-compose up -d
endif


.PHONY: sql
sql:
	docker-compose exec cnx-db /bin/bash -c 'psql --pset expanded=auto $$DB_URL'
