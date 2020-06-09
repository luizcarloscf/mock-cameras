VERSION := 0.0.2
USER := luizcarloscf
IMAGE := mock-cameras
PYTHON := python3
FLAKE8 := $(PYTHON) -m flake8

.PHONY: help, clean, lint, login, build, push  

help:
	@ echo "Usage:\n"
	@ echo "make clean-pyc     Remove python files artifacts."
	@ echo "make clean-docker  Clean all stopped containers and build cache."
	@ echo "make clean         clean-pyc and clean-docker."
	@ echo "make build         Build docker image."
	@ echo "make push          Push docker image to dockerhub."
	@ echo "make login	       Login on docker (necessary to push image)."
	@ echo "make lint          Check style with flake8."

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-docker:
	@ docker system prune

clean: clean-pyc clean-docker 

build:
	docker build -f etc/docker/Dockerfile -t $(USER)/$(IMAGE):$(VERSION) .

push:
	docker push $(USER)/$(IMAGE):$(VERSION)

login:
	docker login

lint:
	@ $(FLAKE8) src/mock_cameras/

install:
	./bootstrap.sh

proto:
	@ docker run --rm -v $(PWD):$(PWD) -w $(PWD) luizcarloscf/docker-protobuf:master \
												--python_out=./src/mock_cameras \
												-I./src/conf/ info.proto
	@ echo "src/is-gesture/options_pb2.py file successfully written"