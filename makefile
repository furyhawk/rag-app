IMAGE_REPO ?= rag-faq
FUNCTION_NAME ?= rag-faq
IMAGE_TAG ?= latest
PLATFORM ?= linux/arm64

serve:
	poetry run uvicorn app.server:app --host 0.0.0.0 --port 8080

run: build-image
	docker run -p 8080:8080 ${IMAGE_REPO}:${IMAGE_TAG} -d

build-image:
	docker image build --platform ${PLATFORM} -t ${IMAGE_REPO}:${IMAGE_TAG} .