.PHONY: install test lint format run clean build start-local stop-local

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run ruff check src tests

format:
	poetry run ruff format src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache

build: clean lint test
	docker build -t python-service-template:latest .

start-local: build
	docker compose -f deployment/docker_compose/docker-compose.local.yml up -d

stop-local: clean
	docker compose -f deployment/docker_compose/docker-compose.local.yml down
