PYTHON=/usr/bin/env python
PIP=/usr/bin/pip
PACKAGES=python python-pip
DEPENDENCIES=requirements.txt
MOD_NAME=flasking
VERSION_NUMBER?="0.9.99"


.PHONY: info install test wheel

clean-build:
		rm -rf build/ dist/
		rm -rf $(MOD_NAME)-$(VERSION_NUMBER)_* $(MOD_NAME).egg-info

info:
		@echo "****************************************************************"
		@echo "To build this project you need these dependencies: $(PACKAGES)"
		@echo "Check requirements.txt/setup.py file to see python dependencies."
		@echo "Npm build dependencies are: $(NPM_PACKAGES)"
		@echo "****************************************************************"
		@echo "USAGE:"
		@echo "- To install dependencies: make install"
		@echo "- To build the egg/wheel: make egg | make wheel"
		@echo "- To launch: make [start|stop|debug]"
		@echo "- To test: make test   **unit(integration)test"

start:
		$(PYTHON) flask-me.py

make-db:
		$(PYTHON) -c 'from flasking.db.database import init_db; init_db()' 

install: build-reqs info
		@echo "Python dependencies"
		$(PIP) install -r $(DEPENDENCIES)
		
build-reqs:
		$(PIP) install --upgrade pip
		$(PIP) install --upgrade setuptools
		# pip you are so stupid http://stackoverflow.com/a/25288078
		$(PIP) install --upgrade setuptools
		$(PIP) install wheel

test: build-reqs
		touch conftest.py
		py.test test 
		rm conftest.py

egg: clean-build
		$(PYTHON) setup.py bdist_egg --exclude-source-files > build.log

wheel: build-reqs egg
		$(PIP) wheel --wheel-dir=$(MOD_NAME)-$(VERSION_NUMBER) -r $(DEPENDENCIES)
		wheel convert dist/*.egg
		