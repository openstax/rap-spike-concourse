.PHONY: help_submake
help_submake:
	@echo "make build-sdist           Build the source distribution of the content event resource"
	@echo "make build-image           Build the image according to the version number"
	@echo "make tag-latest            Tag the currently built image with latest"
	@echo "make release-latest        Release the latest tagged image to docker hub"
	@echo "make release               Release the tagged version image to docker hub"
	@echo "make test                  Run the tests"

ORG_NAME := openstax
VERSION := 0.1.0
NAMESPACE := content-event-resource
BUILD_ARGS := $(BUILD_ARGS)
MAJOR := $(word 1,$(subst ., ,$(VERSION)))
MINOR := $(word 2,$(subst ., ,$(VERSION)))
MAJOR_MINOR_PATCH := $(word 1,$(subst -, ,$(VERSION)))

.PHONY: build-sdist
build-sdist:
	python setup.py sdist

.PHONY: build-image
build-image: build-sdist
	docker build $(BUILD_ARGS) -t $(ORG_NAME)/$(NAMESPACE):$(VERSION) .

.PHONY: tag-latest
tag-latest: build-image
	docker tag $(ORG_NAME)/$(NAMESPACE):$(VERSION) $(ORG_NAME)/$(NAMESPACE):latest

.PHONY: release-latest
release-latest: tag-latest
	docker push $(ORG_NAME)/$(NAMESPACE):latest

.PHONY: release
release:
	@if ! docker images $(ORG_NAME)/$(NAMESPACE) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(ORG_NAME)/$(NAMESPACE) version $(VERSION) is not yet built. Please run 'make build-image'"; false; fi
	docker push $(ORG_NAME)/$(NAMESPACE):$(VERSION)

.PHONY: test
test:
	python -m pytest -vvv ./tests
