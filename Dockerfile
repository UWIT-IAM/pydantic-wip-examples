FROM uwitiam/poetry:latest AS app-base
WORKDIR /pydantic-examples
COPY ./ ./
RUN poetry install

FROM app-base
EXPOSE 5000
