.PHONY: help install dev lint format type-check test ci clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -e .

dev: ## Install development dependencies
	pip install -e ".[dev]"

lint: ## Run linter (ruff check)
	ruff check src tests

format: ## Format code (ruff format)
	ruff format src tests
	ruff check --fix src tests

type-check: ## Run type checker (mypy)
	mypy src

test: ## Run tests
	pytest tests -v

test-cov: ## Run tests with coverage
	pytest tests -v --cov=src --cov-report=term-missing --cov-report=html

ci: lint type-check test ## Run all CI checks (lint, type-check, test)

all: ci ## Alias for ci

clean: ## Clean build artifacts
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

# Development commands
transcribe: ## Transcribe an MP3 file (Usage: make transcribe INPUT=audio.mp3)
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: INPUT argument required"; \
		echo "Usage: make transcribe INPUT=audio.mp3"; \
		echo "       make transcribe INPUT=audio.mp3 OUTPUT=subtitle.srt"; \
		exit 1; \
	fi
	@if [ -n "$(OUTPUT)" ]; then \
		python -m transcribe "$(INPUT)" -o "$(OUTPUT)"; \
	else \
		python -m transcribe "$(INPUT)"; \
	fi
