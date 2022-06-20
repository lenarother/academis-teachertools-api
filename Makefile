.PHONY: coverage coverage-html devinit devinstall tests

help:
	@echo "devinstall - install requirements and create settings.py"
	@echo "devinit - apply migrations"
	@echo "test - run tests"
	@echo "coverage - calculate coverage"
	@echo "coverage-html - calculate coverage html"


devinstall:
	pip install --upgrade pip setuptools wheel
	pip install -e .
	pip install -r resources/requirements-dev.txt

	sh -c 'if [ ! -f src/teachertools/settings.py ]; then echo "from teachertools.conf.dev_settings import *" > src/teachertools/settings.py; fi'


devinit:
	python src/manage.py migrate


tests:
	py.test ${ARGS}


coverage:
	py.test --cov ${ARGS}


coverage-html:
	py.test --cov --cov-report=html ${ARGS}


