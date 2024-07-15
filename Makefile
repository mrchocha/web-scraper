# Makefile for FastAPI project

# Variables
VENV := .venv
PYTHON := $(VENV)/bin/python3.12
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn

# Default target
.PHONY: all
all: install run

# Create virtual environment
$(VENV):
	python3 -m venv $(VENV)

# Install dependencies
.PHONY: install
install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run the FastAPI application
.PHONY: run
run:
	$(UVICORN) app.main:app --reload

# Format the code
.PHONY: format
format:
	$(PYTHON) -m black .

# Lint the code
.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

# Clean up virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV)

# Create requirements.txt
.PHONY: freeze
freeze: $(VENV)
	$(PIP) freeze > requirements.txt


