IMAGE_REPO ?= rag-faq
FUNCTION_NAME ?= rag-faq
IMAGE_TAG ?= latest
PLATFORM ?= linux/arm64

run:
	docker run -p 8080:8080 ${IMAGE_REPO}:${IMAGE_TAG} -d

build-image:
	docker image build --platform ${PLATFORM} -t ${IMAGE_REPO}:${IMAGE_TAG} .