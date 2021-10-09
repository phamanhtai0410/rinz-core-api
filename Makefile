SHELL=/bin/bash -o pipefail

.PHONY: build
build:
		docker build -t ${CI_REGISTRY}/rzmusic/${APP_NAME}:${CI_COMMIT_SHORT_SHA} .

.PHONY: push
push:
		docker push ${CI_REGISTRY}/rzmusic/${APP_NAME}:${CI_COMMIT_SHORT_SHA}
