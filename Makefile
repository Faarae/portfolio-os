.PHONY: install format lint test run

PYTHON = python
PIP = pip
PRE_COMMIT = pre-commit
PYTEST = pytest
BLACK = black
RUFF = ruff
MYPY = mypy

install:
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PRE_COMMIT) install

format:
	$(BLACK) .
	$(RUFF) check --fix .

lint:
	$(RUFF) check .
	$(MYPY) src tests

test:
	$(PYTEST)

run:
	$(PYTHON) -m src.main $(ARGS)
