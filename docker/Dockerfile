## base image
FROM python:slim-buster AS compile-image

## install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential

RUN addgroup --gid 1000 zucced_api
RUN adduser --uid 1000 \
            --gid 1000 \
            --home /home/zucced_api \
            --quiet \
            --disabled-password \
            zucced_api

USER zucced_api
WORKDIR /home/zucced_api

## virtualenv
ENV VIRTUAL_ENV=/home/zucced_api/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir app
WORKDIR /home/zucced_api/app

## add and install requirements
RUN pip install --upgrade pip

COPY --chown=zucced_api:zucced_api requirements.install .
RUN pip install -r requirements.install

COPY --chown=zucced_api:zucced_api . .
RUN pip install -e '.[dev]'

ENTRYPOINT ["./docker/entrypoint.sh"]
