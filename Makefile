.PHONY: tests

tests:
	pytest tests

format:
	black api tests

lint:
	flake8 api tests --max-line-length 100
