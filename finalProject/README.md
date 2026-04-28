# World Health Data Analysis
This project utilizes a FastAPI application that allows the user to load, store, and retrieve global health data through a Redis database. This app includes a job system where the user can submit a job based on country and year range. These jobs are then added to a queue in Redis and processed by a worker. The worker updates the statuses of the jobs. The database includes health indicators such as life expectancy, mortality rates, and disease prevalence. The application is containerized using Docker to ensure reproducibility.

### Tools Used
- FastAPI: framework used to set up a RESTful API using routes
- REDIS: database used to store data
- Docker: used to containerize the application for replication
- HotQueue: queue for processing jobs asynchronously

### Redis Database Usages
This project uses Redis for:

- Raw Data Database: stores all health records
- Jobs Database: stores job data and statuses
- Queue (HotQueue): manages asynchronous job execution
- Results Database: stores generated plots and results

### Structure
- Dockerfile: Has everything necessary to build and run docker image which runs the FastAPI application 
- docker-compose.yml: defines and run containers 
- api.py: FastAPI app that loads, stores, and retrieves world health data and handles job requests 
- jobs.py: handles job creation, storage, and queueing using Redis 
- worker.py: processes jobs from the queue and updates their status 
- world_health_data.csv: dataset used to fill database 
- pyproject.toml: provides standards for configuring 
- uv.lock: contains all uv dependencies 
- .python-version: contains version of python to use 
- test/test_FastAPI_api.py: tests fastAPI routes and responses
- test/test_jobs.py: tests posting a job, getting a job, getting status, and testing results
- test/test_worker.py: tests worker and how it processes a job
- requirements.txt: lists Python dependencies needed to run the project

### Data
The dataset is sourced from Kaggle: https://www.kaggle.com/datasets/bushraqurban/world-health-indicators-dataset.
The data is accessed locally from a csv file and loaded into Redis.
Each country record includes: country, country_code, year, health_exp, life_expect, maternal_mortality, infant_mortality, neonatal_mortality, under_5_mortality, prev_hiv, inci_tuberc, and prev_undernourishment.
Any missing fields are converted to None and then fed into the model.

### How to build and run a container on docker
To build and start the container you need to run: ``` docker compose up --build ``` .
To stop the container you need to run: ``` docker compose down ``` . 

### How to run on Kubernetes
Apply the pods to create them:
kubectl apply -f kubernetes/prod/
kubectl apply -f kubernetes/test/

Check pods:
kubectl get pods

Check services:
kubectl get services

Check ingress:
kubectl get ingress

The is application is available at:
http://pressleywelsh524.coe332.tacc.cloud

### Using application at a public endpoint
After completing the steps above, the API is accessible at:
http://pressleywelsh524.coe332.tacc.cloud

Example:
curl http://pressleywelsh524.coe332.tacc.cloud/data

### Routes
- ``` GET /help ```
Returns full list of routes.
- ``` POST /data ```
Loads data from the CSV into Redis as pydantic models.
- ``` GET /data ```
Returns all records in Redis.
- ``` DELETE /data ```
Deletes all records from Redis.
- ``` GET /countries ```
Returns all keys in country_code:year format.
- ``` GET /countries/{country_code}/{year} ```
Returns a record for a given country for a given year.
- ``` GET /countries/{country_code} ```
Returns every year of data for a given country.
- ``` POST /jobs ```
Creates a new job using a country code and year range.
- ``` GET /jobs ```
Returns a list of all job IDs.
- ``` GET /jobs/{jobid} ```
Returns the information and status for a given job.
- ``` GET /countries/year/{year} ```
Returns all country records for one year.
- ``` GET /results/{jobid} ```
Returns the result for a completed job of given id.
- ``` GET /download/{jid} ```
Downloads the output.png for a completed job of given id.


### Job System
This application includes a job queue system using Redis and HotQueue. Each job computes summary statistics for a given country over a given period, such as number of records, average health expenditure, and minimum/maximum life expectancy.

When a job is submitted:
- A job ID is created
- The job is stored in Redis
- The job ID is placed into the queue
- A worker retrieves the job from the queue
- The worker updates the job status from QUEUED to RUNNING to FINISHED
- Generates a plot
- Stores the plot image in results database

### Running Locally
Ensure Docker is installed, then run:
docker compose up --build

The API will be available at:
http://localhost:5000

### Example Usage

Load Data:
Docker
```
curl localhost:5000/data -X POST
```

Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/data -X POST
```

Output:
```
{
  "data_loaded": 6650
}
```

Get All Data:
Docker
```
curl localhost:5000/data
```

Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/data
```

Output:
```
[
  {
    "country": "Jamaica",
    "country_code": "JAM",
    "year": 2016,
    "health_exp": null,
    "life_expect": null,
    "maternal_mortality": null,
    "infant_mortality": null,
    "neonatal_mortality": null,
    "under_5_mortality": null,
    "prev_hiv": null,
    "inci_tuberc": 3.2,
    "prev_undernourishment": null
  }
]
```

Get All Country Keys:
Docker
```
curl localhost:5000/countries
```

Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/countries
```

Output:
```
[
  "USA:2015",
  "USA:2016"
]
```

Get One Country-Year Record:
Docker
```
curl localhost:5000/countries/USA/2018
```

Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/countries/USA/2018
```

Output:
```
{
  "country": "United States",
  "country_code": "USA",
  "year": 2018,
  "health_exp": 14.57,
  "life_expect": 77.48,
  "maternal_mortality": 13.0,
  "infant_mortality": 6.7,
  "neonatal_mortality": 4.5,
  "under_5_mortality": 8.0,
  "prev_hiv": null,
  "inci_tuberc": 5.5,
  "prev_undernourishment": 2.5
}
```

Submit a Job:
Docker
```
curl localhost:5000/jobs -X POST -d '{"country_code":"USA","start_year":2015,"end_year":2019}' -H "Content-Type: application/json"
```

Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/jobs -X POST -d '{"country_code":"USA","start_year":2015,"end_year":2019}' -H "Content-Type: application/json"
```

Output:
```
{
  "jid": "ea14dfef-499c-4779-90b7-acfa464c3f4c",
  "status": "QUEUED",
  "country_code": "USA",
  "start_year": 2015,
  "end_year": 2019,
  "start_time": null,
  "end_time": null
}
```

Get Job Status:
Docker
```
curl localhost:5000/jobs/ea14dfef-499c-4779-90b7-acfa464c3f4c
```
Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/jobs/ea14dfef-499c-4779-90b7-acfa464c3f4c
```

Output:
```
{
"jid":"ea14dfef-499c-4779-90b7-acfa464c3f4c",
"status":"FINISHED -- SUCCESS",
"country_code":"USA",
"start_year":2015,
"end_year":2019,
"start_time":"2026-04-28T02:31:55.253220",
"end_time":"2026-04-28T02:31:56.553240"
}
```

Get Job Result:
Docker
```
curl localhost:5000/results/ea14dfef-499c-4779-90b7-acfa464c3f4c
```
Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/results/ea14dfef-499c-4779-90b7-acfa464c3f4c
```

Output:
```
{
"country_code":"USA",
"start_year":2015,
"end_year":2019,
"count":5,
"correlation":-0.6283391557457708,
"min_life_expect":78.5390243902439,
"max_life_expect":78.7878048780488,
"avg_health_exp":16.671135711999998
}
```

Download Plot:
Docker
```
curl localhost:5000/download/ea14dfef-499c-4779-90b7-acfa464c3f4c -o output.png
```

Kubernetes
```
curl http://pressleywelsh524.coe332.tacc.cloud/download/ea14dfef-499c-4779-90b7-acfa464c3f4c -o output.png
```

Output:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 26262  100 26262    0     0  1406k      0 --:--:-- --:--:-- --:--:-- 1424k
```

Run Tests:
```
PYTHONPATH=.:src REDIS_IP=localhost uv run pytest
```
We were receiving recurring errors with uv run pytest alone, so we used Claude to help us resolve this error. Claude suggested we use ```PYTHONPATH=.:src REDIS_IP=localhost``` , and this resulted in all of our tests passing.

### Diagram
<img width="641" height="273" alt="Diagram" src="https://github.com/user-attachments/assets/4f5d9f7b-40a7-40a3-8c9c-f5ffb05f6b13" />
