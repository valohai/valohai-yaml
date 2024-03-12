UV := $(shell command -v uv)
ifdef UV
	PIP_INSTALL = uv pip install
else
	PIP_INSTALL = pip install
endif

.PHONY: help
help:
	@echo "check README for usage"

.PHONY: dev
dev:
	$(PIP_INSTALL) -e . -r requirements-test.txt pre-commit
	pre-commit install

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	pytest
