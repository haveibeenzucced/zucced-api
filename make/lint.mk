lint: install-local
	black --check -q src/
	flake8 src
