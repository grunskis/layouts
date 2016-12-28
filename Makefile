.PHONY:	test

default: test

test:
	python -m unittest discover -v
