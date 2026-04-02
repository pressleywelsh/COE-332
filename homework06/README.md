# World Health Data Analysis
This project utilizes a FastAPI application that allows the user to load, store, and retrieve global health data through a Redis database. The database includes health indicators such as life expectancy, mortality rates, and disease prevalence. The application is containerized using Docker to ensure reproducibility.

### Structure
Dockerfile: Has everything necessary to build and run docker image which runs the FastAPI application
docker-compose.yml: defines and run containers
health_analysis.py: FastAPI application that requests and processes world health data with Redis
world_health_data.csv: dataset used to fill database
pyproject.toml: provides standards for configuring
uv.lock: contains all uv dependencies
.python-version: contains version of python to use

### Data
The dataset is sourced from Kaggle: https://www.kaggle.com/datasets/bushraqurban/world-health-indicators-dataset.
The data is accessed locally from a csv file and loaded into Redis.
Each country record includes: country, country_code, year, health_exp, life_expect, maternal_mortality, infant_mortality, neonatal_mortality, under_5_mortality, prev_hiv, inci_tuberc, and prev_undernourishment.
Any missing fields are converted to None and then fed into the model.

### How to build and run a container
To build and start the container you need to run: ``` docker compose up --build ``` .
To stop the container you need to run: ``` docker compose down ``` . 

### Routes
``` GET /help ```
Returns full list of routes.
``` POST /data ```
Loads data from the CSV into Redis as pydantic models.
``` GET /data ```
Returns all records in Redis.
``` DELETE /data ```
Deletes all records from Redis.
``` GET /countries ```
Returns all keys in country_code:year format.
``` GET /countries/{country_code}/{year} ```
Returns a record for a given country for a given year.
``` GET /countries/{country_code} ```
Returns every year of data for a given country.
