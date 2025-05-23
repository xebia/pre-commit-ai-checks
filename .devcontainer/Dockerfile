FROM --platform=linux/arm64 jhginn/devcontainer:ubuntu2204-pyuv311-20250107-gcloud

RUN apt-get update \
    && apt-get -y install libpq-dev postgresql \
    && rm -rf /var/lib/apt/lists/*

ENV RUFF_CACHE_DIR=$HOME/workspace/.cache/ruff
ENV MYPY_CACHE_DIR=$HOME/workspace/.cache/mypy
ENV PRE_COMMIT_HOME=$HOME/workspace/.cache/pre-commit

RUN pipx install --force uv==0.5.18
