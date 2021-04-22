test: test-${TARGET}

test-docker: ${VERSION} requirements.install
	@docker-compose exec -T zucced_api make TARGET=local test

test-local: ${VERSION} requirements.install
	@pip install -e .
	@python setup.py test

test-ci: test-local

test-production:
