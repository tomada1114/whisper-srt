.PHONY: help install dev lint format type-check test ci clean build publish release

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

# Release commands
build: clean ## Build package
	pip install --quiet build
	python -m build

publish: ## Upload to PyPI (requires TWINE_USERNAME and TWINE_PASSWORD or ~/.pypirc)
	pip install --quiet twine
	twine upload dist/*

release: ## Full release: bump version, CI, build, publish, tag (Usage: make release VERSION=0.3.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION argument required"; \
		echo "Usage: make release VERSION=0.3.0"; \
		exit 1; \
	fi
	@echo "==> Updating version to $(VERSION)..."
	@sed -i '' 's/^version = ".*"/version = "$(VERSION)"/' pyproject.toml
	@echo "==> Running CI checks..."
	$(MAKE) ci
	@echo "==> Building package..."
	$(MAKE) build
	@echo "==> Publishing to PyPI..."
	$(MAKE) publish
	@echo "==> Creating git commit and tag..."
	git add pyproject.toml
	git commit -m "chore: bump version to $(VERSION)"
	git tag -a "v$(VERSION)" -m "Release v$(VERSION)"
	git push && git push --tags
	@echo "==> Release v$(VERSION) complete!"
