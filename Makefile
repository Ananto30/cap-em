SHELL := /bin/bash

IP := $(shell ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | tail -1)
# env
export DB_URI=postgresql://capem:pass@$(IP):5432/postgres
export CONFIG := $(shell cat ./config/example.config.yml | base64)


setup:
	python3 -m venv venv
	source venv/bin/activate && ( \
		pip install -r requirements.txt; \
		pip install -r tests/requirements.txt; \
		pip install black isort flake8 pylint pytype mypy; \
		)

test:
	python3 -m pytest tests --cov=src --cov-report=term-missing -vv

run:
	@echo Config: $(CONFIG)
	@echo DB_URI: $(DB_URI)
	uvicorn src.asgi:app --reload

format:
	isort . --profile black -l 99
	black .

install-lint:
	python -m pip install --upgrade pip
	pip install -r requirements.txt  # needed for pytype
	pip install black isort flake8 pylint pytype mypy

lint:
	flake8 ./src ./tests
	pylint ./src ./tests
	# pytype ./src ./tests
	mypy ./src ./tests

docker-build:
	docker build -t capem/falcon .

docker-run:
	docker-compose up -d
	until docker exec capem-postgres pg_isready --username=capem --host=localhost; do sleep 1; done
	@echo Config: $(CONFIG)
	@echo DB_URI: $(DB_URI)
	docker run --name capem -e DB_URI -e CONFIG -p 8000:8000 capem/falcon

docker-stop:
	docker-compose down
	docker rm -f capem

prod-image-run:
	docker-compose up -d
	until docker exec capem-postgres pg_isready --username=capem --host=localhost; do sleep 1; done
	docker pull ananto30/cap-em
	@echo Config: $(CONFIG)
	@echo DB_URI: $(DB_URI)
	docker run --name capem -e DB_URI -e CONFIG -p 8000:8000 ananto30/cap-em
