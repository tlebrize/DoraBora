FROM python:3.11-slim as python-base
ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME=/opt/poetry \
    SHELL=/bin/bash \
    POETRY_VERSION=1.5.1
ENV	PATH="$POETRY_HOME/bin:$PATH"

ARG UNAME=clientuser
ARG UID=1000
ARG GID=1000

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
    \
    && curl -sSL https://install.python-poetry.org | python3 -

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER $UNAME
WORKDIR /workspace

COPY ./poetry.lock ./pyproject.toml /workspace/
RUN poetry install --no-interaction --with dev

COPY ./ /workspace/

EXPOSE 5051 5052

CMD poetry run python main.py
