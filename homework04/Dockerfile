FROM python:3.14

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Initialize a uv project
RUN uv init /code

# NOTE: The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile
WORKDIR /code

RUN uv add pydantic pytest requests xmltodict

COPY test_iss_tracker.py /code/test_iss_tracker.py
COPY iss_tracker.py /code/iss_tracker.py

ENV PATH="/code:$PATH"
