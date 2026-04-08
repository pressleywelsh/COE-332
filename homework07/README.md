# World Health Data Analysis
This project utilizes a FastAPI application that allows the user to load, store, and retrieve global health data through a Redis database. This app includes a job system where the user can submit a job based on country and year range. These jobs are then added to a queue in Redis and processed by a worker. The worker updates the statuses of the jobs. The database includes health indicators such as life expectancy, mortality rates, and disease prevalence. The application is containerized using Docker to ensure reproducibility.

### Structure
Dockerfile: Has everything necessary to build and run docker image which runs the FastAPI application
docker-compose.yml: defines and run containers
api.py: FastAPI app that loads, stores, and retrieves world health data and handles job requests
jobs.py: handles job creation, storage, and queueing using Redis
worker.py: processes jobs from the queue and updates their status
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
``` POST /jobs ```
Creates a new job using a country code and year range.
``` GET /jobs ```
Returns a list of all job IDs.
``` GET /jobs/{jobid} ```
Returns the information and status for a given job.

### Job System
This application includes a job queue system using Redis and HotQueue.

When a job is submitted:
- A job ID is created
- The job is stored in Redis
- The job ID is placed into the queue
- A worker retrieves the job from the queue
- The worker updates the job status from QUEUED to RUNNING to FINISHED

### Example Usage

Load data:
```
curl localhost:5000/data -X POST
```
Output:
```
{
  "data_loaded":6650
}
```

Get all data:
```
curl localhost:5000/data
```
Output:
```
[
  {
    "country":"Jamaica",
    "country_code":"JAM",
    "year":2023,
    "health_exp":null,
    "life_expect":null,
    "maternal_mortality":null,
    "infant_mortality":null,
    "neonatal_mortality":null,
    "under_5_mortality":null,
    "prev_hiv":null,
    "inci_tuberc":3.2,
    "prev_undernourishment":null
  },
  ...
]
```

Get all country keys:
```
curl localhost:5000/countries
```
Output:
```
[
  "USA:2000",
  "USA:2001",
  ...
]
```

Get one country-year record:
```
curl localhost:5000/countries/USA/2005
```
Output:
```
{
  "country":"United States",
  "country_code":"USA",
  "year":2005,
  "health_exp":14.57938957,
  "life_expect":77.4878048780488,
  "maternal_mortality":13.0,
  "infant_mortality":6.7,
  "neonatal_mortality":4.5,
  "under_5_mortality":8.0,
  "prev_hiv":null,
  "inci_tuberc":5.5,
  "prev_undernourishment":2.5
}
```

Submit a job:
```
curl localhost:5000/jobs -X POST -H "Content-Type: application/json" -d '{"country_code":"USA","start_year":2000,"end_year":2010}'
```
Output:
```
{
  "jid": "4937df6c-03ff-4dd6-9a04-292ba3d18935",
  "status": "QUEUED",
  "country_code": "USA",
  "start_year": 2000,
  "end_year": 2010,
  "start_time": null,
  "end_time": null
}
```

Get job by ID:
```bash
curl localhost:5000/jobs/4937df6c-03ff-4dd6-9a04-292ba3d18935
```
Output:
```
{
  "jid": "4937df6c-03ff-4dd6-9a04-292ba3d18935",
  "status": "FINISHED -- SUCCESS",
  "country_code": "USA",
  "start_year": 2000,
  "end_year": 2010,
  "start_time": "2026-04-08T10:00:00",
  "end_time": "2026-04-08T10:00:05"
}
```
