devinstall:
	sh -c 'if [ "`which msgfmt`" == "" ]; then brew install gettext && brew link gettext --force; fi'

	pip install --upgrade pip setuptools wheel
	pip install -e .
	pip install -r resources/requirements-develop.txt

	sh -c 'if [ ! -f src/teachertools/settings.py ]; then echo "from teachertools.conf.dev_settings import *" > src/teachertools/settings.py; fi'


devinit:
	python src/manage.py migrate


tests:
	py.test ${ARGS}


coverage:
	py.test --cov ${ARGS}


coverage-html:
	py.test --cov --cov-report=html ${ARGS}


