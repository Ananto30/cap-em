SHELL := /bin/bash

setup:
	python3 -m venv venv
	source venv/bin/activate && ( \
		pip install -r requirements.txt; \
		pip install -r tests/requirements.txt; \
		pip install black isort flake8; \
		)

test:
	python3 -m pytest tests --cov=app --cov-report=term-missing -vv

format:
	python3 -m black . --line-length 90
	python3 -m isort . --profile black --line-length 90
	python3 -m flake8 ./app --max-line-length 90

run:
	mkdir ./app/config || true
	cp ./config/config.txt ./app/config/
	gunicorn --chdir app web_app:app -w 2 --threads 2 -b 0.0.0.0:8003

docker-build:
	docker build -t capem/flask .

docker-run:
	docker run --name capem -v $(pwd)/config:/app/config -p 8003:8003 -e DB_URI=postgres://capem:pass@0.0.0.0:5432/postgres capem/flask