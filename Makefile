.PHONY: test lint format install clean

install:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v --tb=short

coverage:
	python -m pytest tests/ --cov=prompt_engineering_lab --cov-report=term-missing

lint:
	python -m ruff check .
	python -m ruff format --check .

format:
	python -m ruff format .
	python -m ruff check --fix .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info
