# syntax=docker/dockerfile:1.3
FROM python:3.10.9-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000

ENV USER="fakester"
ENV HOME="/home/$USER"
ENV APP_DIR="$HOME/app"
ENV VIRTUAL_ENV="$HOME/venv"

# Create a non root user
RUN groupadd --gid ${GID} $USER
RUN useradd --system --create-home --no-log-init \
    --uid ${UID} --gid ${GID} \
    --shell /bin/bash $USER
USER $USER
WORKDIR $APP_DIR

# Set up the virtualenv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies with `pip-tools`
RUN python -m pip install pip-tools
COPY --chown=$USER:$USER requirements/main.txt $APP_DIR/requirements/main.txt
RUN --mount=type=cache,target=$HOME/.cache,uid=${UID},gid=${GID} \
    python -m piptools sync requirements/main.txt

# Copy the app
COPY --chown=$USER:$USER src/ $APP_DIR/src

#######
# App #
#######
FROM base as app

# Run the app with `gunicorn`
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--pythonpath=src", "--bind=0.0.0.0:8000", "--worker-tmp-dir=/dev/shm", "fakester.wsgi"]

#######
# Dev #
#######
FROM base as dev

# Install dev dependencies
COPY --chown=$USER:$USER requirements/dev.txt $APP_DIR/requirements/dev.txt
RUN --mount=type=cache,target=$HOME/.cache,uid=${UID},gid=${GID} \
    python -m piptools sync requirements/main.txt requirements/dev.txt
