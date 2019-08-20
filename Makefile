init:
	git submodule update --init

configure:
	python -m pip install -r tests/requirements.txt
	python tests/scripts/configenv.py

test:
	tox .
