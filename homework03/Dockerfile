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

RUN uv add pydantic pytest

COPY ml_data_analysis.py /code/ml_data_analysis.py
COPY gcd_algorithm.py /code/gcd_algorithm.py
COPY test_ml_data_analysis.py /code/test_ml_data_analysis.py
COPY test_gcd_algorithm.py /code/test_gcd_algorithm.py

ENV PATH="/code:$PATH"
