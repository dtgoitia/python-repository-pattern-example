requirements:
	rm -f requirements.txt
	pip-compile --no-header --no-emit-index-url --verbose requirements.in --output-file requirements.txt

dev-requirements:
	rm -f dev-requirements.txt
	pip-compile --no-header --no-emit-index-url --verbose dev-requirements.in --output-file dev-requirements.txt

install:
	pip install -r requirements.txt

dev-install: install
	pip install -r dev-requirements.txt

lint:
	flake8
	black --check --diff .
	isort --check --diff .
	python -m mypy --config-file setup.cfg --pretty .

format:
	isort .
	black .

test:
	pytest tests -vv
