.PHONY: clean build test publish install dev

clean:
	rm -rf dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

test: build
	pip install dist/bloggy-*.whl --force-reinstall
	bloggy demo/

install:
	pip install -e ".[dev]"

dev:
	bloggy demo/

publish: build
	python -m twine upload --repository sizhky dist/*

publish-test: build
	python -m twine upload --repository testpypi dist/*
