configure:
	python -m pip install -r requirements.txt
	python tests/scripts/configenv.py

test:
	tox .
