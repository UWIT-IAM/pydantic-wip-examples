FROM uwitiam/poetry:latest AS app-base
WORKDIR /pydantic-examples
COPY pyproject.toml poetry.lock ./
RUN poetry install
EXPOSE 5000
