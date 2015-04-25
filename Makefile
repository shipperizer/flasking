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
# f***ing makefile, I love u but u r bugging me too much
# http://stackoverflow.com/questions/4483313/make-error-for-ifeq-syntax-error-near-unexpected-token
ifeq ($(SUDO_USER), root)
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	@echo "WARN: YOU ARE EXECUTING AS root, IT'S ADVISABLE TO RUN IT AS A NORMAL USER AND USE SUDO"
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	@echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
endif
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
		$(PYTHON) setup.py test 
		rm conftest.py

egg: clean-build
		$(PYTHON) setup.py bdist_egg --exclude-source-files > build.log

wheel: build-reqs egg
		$(PIP) wheel --wheel-dir=$(MOD_NAME)-$(VERSION_NUMBER) -r $(DEPENDENCIES)
		wheel convert dist/*.egg
		