# Makefile to build the project

## Environment variables
PROJECT_NAME=aws-data-streaming-app
PYTHON_INTERPRETER=python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL:=/bin/bash
PIP:=pip

## Create python interpreter environment.
create-environment:
	@echo ">>> Project: $(PROJECT_NAME)..."
	@echo ">>> Python version:"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv"
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV:=source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && export PYTHONPATH=${PYTHONPATH} && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./dev-requirements.txt)

################################################################################################################
# Set Up
## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
# safety:
# 	$(call execute_in_env, $(PIP) install safety)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

## Set up dev requirements (bandit, safety, black)
dev-setup: bandit black coverage # safety
	$(call execute_in_env, $(PIP) install -r ./dev-requirements.txt)

# Build / Run

## Run the security test (bandit + safety)
security-test:
# $(call execute_in_env, safety check  -r ./dev-requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the black code check
run-black:
	$(call execute_in_env, black  ./lambda_function.py ./test/*/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, pytest test/* -vv --testdox)

## Run the coverage check
check-coverage:
	$(call execute_in_env, coverage run --omit 'venv/*' -m pytest test/* && coverage report -m)

## Run all checks
run-checks: run-black unit-test check-coverage security-test
