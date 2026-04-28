FROM python:3.14

# COPY the uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project files
RUN mkdir /app
COPY pyproject.toml /app
COPY .python-version /app
COPY uv.lock /app
COPY world_health_data.csv /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync

# COPY source code
COPY src /app/src

CMD ["uv", "run", "--", "fastapi", "dev", "--host", "0.0.0.0", "src/FastAPI_api.py"]
