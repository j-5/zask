.PHONY: test docs

all: test

test:
	tox

release:
	python bin/release.py
	python3 bin/release.py

docs:
	$(MAKE) -C docs html
