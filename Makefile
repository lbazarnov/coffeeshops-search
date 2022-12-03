install:
	poetry install

coffeeshops-search:
	poetry run python3 coffeeshops_search/main.py

build:
	poetry build

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 coffeeshops_search
