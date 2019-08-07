.PHONY: help_submake
help_submake:
	@echo "make build             Build the docker image for content-event concourse resource"
	@echo "make publish           Publish the docker image for content-event concourse resource to dockerhub"

.PHONY: build
build:
	python setup.py sdist
	docker build -t openstax/content-event-resource .

.PHONY: publish
publish: build
	docker push openstax/content-event-resource

