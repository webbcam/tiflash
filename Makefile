configure:
	git submodule update --init
	python -m pip install -r tests/requirements.txt
	python tests/scripts/configenv.py

test:
	tox .
