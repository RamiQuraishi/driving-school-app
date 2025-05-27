.PHONY: install test lint format clean build dev

# Python environment
install:
	poetry install
	npm install

# Testing
test:
	poetry run pytest

# Linting and formatting
lint:
	poetry run flake8 ramidriveschool tests
	poetry run mypy ramidriveschool tests
	poetry run black --check ramidriveschool tests
	poetry run isort --check-only ramidriveschool tests

format:
	poetry run black ramidriveschool tests
	poetry run isort ramidriveschool tests

# Development
dev:
	poetry run uvicorn ramidriveschool.main:app --reload

# Building
build:
	npm run build

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} + 