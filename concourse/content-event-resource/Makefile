.PHONY: help_submake
help_submake:
	@echo "make build-sdist           Build the source distribution of the content event resource"
	@echo "make build-dev             Build and tag the dev docker image for content-event concourse resource"
	@echo "make publish-dev           Publish the dev docker image for content-event concourse resource to dockerhub"
	@echo "make build-latest          Build and tag the latest docker image for content-event concourse resource"
	@echo "make publish-latest        Publish the latest docker image for content-event concourse resource to dockerhub"


.PHONY: build-sdist
build-sdist:
	python setup.py sdist

.PHONY: build-sdist
build-dev:
	docker build -t openstax/content-event-resource:dev .

.PHONY: publish-dev
publish-dev: build-dev
	docker push openstax/content-event-resource:dev

.PHONY: build-sdist
build-latest:
	docker build -t openstax/content-event-resource:latest .

publish-latest: build-sdist
	docker push openstax/content-event-resource:latest

.PHONY: test
test:
	python -m pytest -vvv ./tests
