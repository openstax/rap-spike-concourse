.PHONY: default
default: help

.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make services          Run the services that Concourse and the pipeline requires"
	@echo "make initdb            Restore DB dump on first run, can be also used to restore DB"
	@echo "make sql               Connect to the cnx-db database with a psql shell"


dump.sql.gz:
	@echo Downloading db dump...
	rsync -tv --progress -e 'ssh -T -c aes128-ctr -o Compression=no -x' backup1.cnx.org:/var/backups/db_dump/20190805_dump.sql.gz ./dump.sql.gz


.PHONY: services
services:
	docker-compose up -d
	@echo Info: To (re-)init DB run "make initdb" now.


.PHONY: initdb
initdb: dump.sql.gz
	@echo drop and recreate db then restore dump
	docker-compose exec -u postgres cnx-db dropdb -U postgres repository
	docker-compose exec -u postgres cnx-db createdb -U postgres -O rhaptos repository
	gunzip <dump.sql.gz | docker-compose exec -T -u postgres cnx-db psql -U postgres repository


.PHONY: sql
sql:
	docker-compose exec cnx-db /bin/bash -c 'psql --pset expanded=auto $$DB_URL'
