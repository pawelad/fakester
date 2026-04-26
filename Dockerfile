# syntax=docker/dockerfile:1.3
FROM python:3.12.6-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000

ENV USER="fakester"
ENV HOME="/home/$USER"
ENV APP_DIR="$HOME/app"
ENV VIRTUAL_ENV="$HOME/venv"

# Create a non root user
RUN groupadd --gid ${GID} $USER \
    && useradd --system --create-home --no-log-init \
      --uid ${UID} --gid ${GID} \
      --shell /bin/bash $USER

USER $USER
WORKDIR $APP_DIR

###########
# Builder #
###########
FROM base as builder

COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /bin/uv

# Set up the virtualenv
RUN uv venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT="$VIRTUAL_ENV"

# Install Python dependencies
COPY --chown=$USER:$USER pyproject.toml uv.lock ./
RUN --mount=type=cache,uid=${UID},gid=${GID},target=$HOME/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

###########
#   Dev   #
###########
FROM builder as dev

# Install dev dependencies
RUN --mount=type=cache,uid=${UID},gid=${GID},target=$HOME/.cache/uv \
    uv sync --frozen --no-install-project

###########
#   App   #
###########
FROM base as app

# Copy virtualenv from builder
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the app
COPY --chown=$USER:$USER src/ $APP_DIR/src

# Collect static assets
RUN python src/manage.py collectstatic --noinput

# Run the app with `gunicorn`
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--pythonpath=src", "--bind=0.0.0.0:8000", "--worker-tmp-dir=/dev/shm", "fakester.wsgi"]
