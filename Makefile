SHELL := /bin/bash

venv:
	@echo "Creating virtual environment..."
	@python -m venv venv
	@echo "Virtual environment created successfully."

activate:
	@echo "Activating virtual environment..."
	@source venv/bin/activate
	@echo "Virtual environment activated. Use 'deactivate' to exit."

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt
	@echo "Dependencies installed successfully."

format:
	@echo "Formatting code..."
	@black --line-length 79 --target-version py310 --skip-string-normalization --exclude venv,build,dist,docs .
	@isort --profile black --line-length 79 --skip venv,build,dist,docs .
	@pylint --max-line-length 79 --ignore=E501,W503 --exclude venv,build,dist,docs .
	@echo "Code formatted successfully."