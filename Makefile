.PHONY: default
default: help

.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo 'make services          Run the services that Concourse and the pipeline requires"
	@echo "make sql               Connect to the cnx-db database with a psql shell"

.PHONY: services
services:
	docker-compose up -d

.PHONY: sql
sql:
	docker-compose exec cnx-db psql --pset expanded=auto -U postgres
