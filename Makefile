.PHONY: help
help:
	@echo "check README for usage"

.PHONY: dev
dev:
	pip install -e . -r requirements-test.txt pre-commit
	pre-commit install

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	pytest
