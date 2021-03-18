requirements.txt:
	pip-compile --no-header --no-emit-index-url --verbose requirements.in --output-file requirements.txt

install:
	pip install -r requirements.txt

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
