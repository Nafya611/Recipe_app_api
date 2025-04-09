FROM python:3.11-alpine3.21

LABEL maintainer="Django Docker"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false
ENV DEV=$DEV

# Install system dependencies and Python packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache \
    postgresql-client \
    jpeg-dev && \
    apk add --no-cache --virtual .tmp-build-deps \
    build-base \
    postgresql-dev \
    musl-dev \
    zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
    /py/bin/pip install -r /tmp/requirements.dev.txt --no-cache-dir --verbose ;\
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user
