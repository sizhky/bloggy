.PHONY: clean build test publish install dev bump-major bump-minor bump-patch

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

# Version bumping
bump-major:
	@echo "Bumping major version..."
	@python bump_version.py major

bump-minor:
	@echo "Bumping minor version..."
	@python bump_version.py minor

bump-patch:
	@echo "Bumping patch version..."
	@python bump_version.py patch

publish: bump-patch build
	python -m twine upload --repository sizhky dist/*

publish-test: build
	python -m twine upload --repository testpypi dist/*

publish-and-checkpoint: publish
	zsh -i -c "checkpoint"

pc: publish-and-checkpoint