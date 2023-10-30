all: list-targets

.PHONY: all list-targets venv
list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]'

run:
	set -o allexport && . ./.env && set +o allexport && \
	. venv/bin/activate && \
		python main.py && \
		deactivate

run-docker:
	. venv/bin/activate && \
		python main.py && \
		deactivate

setup: venv dep

venv:
	@python3.11 -m venv ./venv/

dep:
	@. venv/bin/activate && \
		pip install -r requirements.txt && \
		deactivate

version:
	@. venv/bin/activate && \
		python --version && \
		deactivate
