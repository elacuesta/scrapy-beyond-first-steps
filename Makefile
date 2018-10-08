.PHONY: lint

lint:
	@python -m flake8 --exclude=.git,venv-* pybr2018
