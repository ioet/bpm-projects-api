# Make file for bpm-projects-api. Use make help for assistance.

shell := /bin/bash

.PHONY: dev-requirements
dev-requirements:
	pip3 install -r requirements/azure-dev.txt
	pip3 install codecov
	python3 cli.py init_db

.PHONY: run prod
run prod:
	@echo Running in production mode. To run in development mode use make dev.
	gunicorn -b 0.0.0.0:8000 run:app

.PHONY: run-with-opa
run-with-opa: start-opa
	@echo Running in production mode using OPA to enforce security policies.
	gunicorn -b 0.0.0.0:8000 run:app

.PHONY: dev
dev:
	@echo Running in development mode. To run in production mode use make run.
	flask run

.PHONY: opa-linux
opa-linux:
	curl -L -o opa $(shell curl "https://api.github.com/repos/open-policy-agent/opa/releases/latest" | jq -c '.["assets"] | .[]| select(.name | contains("linux")) | .browser_download_url' || https://github.com/open-policy-agent/opa/releases/download/v0.10.1/opa_linux_amd64)
	chmod 755 ./opa
	@echo opa has been installed.

.PHONY: opa-mac
opa-mac:
	curl -L -o opa $(shell curl "https://api.github.com/repos/open-policy-agent/opa/releases/latest" | jq -c '.["assets"] | .[]| select(.name | contains("darwin")) | .browser_download_url' || https://github.com/open-policy-agent/opa/releases/download/v0.10.1/opa_darwin_amd64)
	chmod 755 ./opa
	@echo opa has been installed.

.PHONY: bpm-opa-directory
bpm-opa-directory:
	curl -L -O $(shell curl "https://api.github.com/repos/ioet/bpm-opa/releases/latest" | jq -r ".assets[0].browser_download_url")
	rm -rf bpm
	tar -xvzf bpm.tar.gz
	rm bpm.tar.gz

.PHONY: start-opa
start-opa:
	nohup ./opa run -s -w bpm &
	@echo The opa server is running in http://0.0.0.0:8181

.PHONY: stop-opa
stop-opa:
	@echo Stopping the opa server...
	@kill $(shell ps | grep opa | awk '{print $1}' | head -n 1)

.PHONY: help
help:
	@echo "make run"
	@echo "make prod"
	@echo "       Runs the app in production mode"
	@echo "make dev"
	@echo "       Runs the app in development mode"
	@echo "make bpm-opa-directory"
	@echo "       Downloads the opa policies to the folder bpm"
	@echo "make opa"
	@echo "       Downloads and installs the latest version of opa"
	@echo "make start-opa"
	@echo "       Starts the opa server"
	@echo "make stop-opa"
	@echo "       Stops the opa server"
