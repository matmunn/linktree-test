FROM python:3.10-bullseye

RUN groupadd -r app && \
    useradd -r -g app app && \
    mkdir -p /app /virtualenv && \
    chown -R app: /app /virtualenv

ENV PYTHONFAULTHANDLER 1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    VIRTUALENV_BASE=/virtualenv

WORKDIR /app
ADD . .

RUN set -ex \
    && apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install poetry \
    && ./app.sh install-deps

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000
