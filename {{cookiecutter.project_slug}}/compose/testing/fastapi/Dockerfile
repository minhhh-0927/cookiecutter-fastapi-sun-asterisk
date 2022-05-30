ARG PYTHON_VERSION=3.9-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=testing

WORKDIR /tmp

# Requirements are installed here to ensure they will be cached.
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export --without-hashes -f requirements.txt --output ${BUILD_ENVIRONMENT}.txt --dev

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=testing
ARG APP_HOME=/code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /tmp/${BUILD_ENVIRONMENT}.txt ${APP_HOME}/${BUILD_ENVIRONMENT}.txt

# use wheels to install python dependencies
RUN pip install --no-cache-dir --upgrade -r ${APP_HOME}/${BUILD_ENVIRONMENT}.txt

COPY ./compose/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# copy application code to WORKDIR
COPY . ${APP_HOME}
