from pydantic import BaseModel
import requests
import redis
import json
from fastapi import FastAPI, HTTPException
import csv
import logging
import os
from typing import Optional
from jobs import add_job, get_job_by_id, get_job_ids, Job, get_result

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

def get_redis_client():
    return redis.Redis(host='redis-db', port=6379, db=0)

rd = get_redis_client()

class countryData(BaseModel):
    country: str
    country_code: str
    year: int
    health_exp: Optional[float]
    life_expect: Optional[float]
    maternal_mortality: Optional[float]
    infant_mortality: Optional[float]
    neonatal_mortality: Optional[float]
    under_5_mortality: Optional[float]
    prev_hiv: Optional[float]
    inci_tuberc: Optional[float]
    prev_undernourishment: Optional[float]

class JobInput(BaseModel):
    country_code: str
    start_year: int
    end_year: int


@app.get("/help")
def help():
    return {
        "routes": {
            "/data POST": "load data into Redis",
            "/data GET": "return all data",
            "/data DELETE": "delete all data",
            "/countries GET": "return all country_code:year keys",
            "/countries/{country_code}/{year} GET": "return one record",
            "/jobs POST": "submit a job",
            "/jobs GET": "list all jobs",
            "/jobs/{jobid} GET": "get job info",
            "/countries/{country_code} GET": "return all records for one country",
            "/results/{jobid} GET": "get job result"
        }
    }

@app.post("/data")
def load_data() -> dict:
    """
    Loads world health data from a local CSV file into the Redis database.

    The CSV file is read from the project directory, cleaned to handle missing
    values (empty strings are converted to None), and converted into Pydantic
    countryData objects. Each record is stored in Redis using a key of the format
    "country_code:year".

    Returns:
    dict: A dictionary containing the total number of records loaded into Redis.
    """

    logging.info("Starting data load")

    count = 0
    with open("world_health_data.csv", "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            #Used AI to help with row below due to constant errors
            clean_row = {
                key: (value if value != "" else None)
                for key, value in row.items()
            }

            record = countryData(**clean_row)

            rd.set(
                f"{record.country_code}:{record.year}",
                record.model_dump_json()
            )
            count += 1

    logging.info(f"Loaded {count} records into Redis")

    return {"data_loaded": count}

@app.get("/data")
def get_data() -> list:
    """
    Returns all data stored in Redis

    Returns:
    list: all country data records
    """
    logging.debug("Getting all data from Redis")
    output = []
    for key in rd.keys():
        output.append(json.loads(rd.get(key)))
    return output

@app.delete("/data")
def delete_data() -> dict:
    """
    Deletes all data from Redis

    Returns:
    dict: number of records deleted
    """
    keys = rd.keys()
    logging.warning(f"Deleting {len(keys)} records from Redis")
    for key in keys:
        rd.delete(key)
    return {"data_deleted": len(keys)}

@app.get("/countries")
def get_countries() -> list:
    """
    Returns all country_code:year keys in Redis

    Returns:
    list: all keys representing stored records
    """
    output = []
    for key in rd.keys():
        output.append(key.decode("utf-8"))
    return output

@app.get('/countries/year/{year}')
def get_year_data(year: int) -> list[dict]:
    """
    Returns all country records for one year.

    Args:
        year: year of data

    Returns:
        list: all country data for the specified year
    """
    logging.debug(f"Looking up all countries for year {year}")
    output = []

    for key in rd.keys():
        key = key.decode("utf-8")
        country_code, record_year = key.split(":")

        if int(record_year) == year:
            raw_data = rd.get(key)
            output.append(json.loads(raw_data))

    if len(output) == 0:
        raise HTTPException(status_code=404, detail=f"No data found for year {year}")

    return output

@app.get("/countries/{country_code}/{year}")
def get_country(country_code: str, year: int) -> dict:
    """
    Returns a specific country record for a given year

    Args:
    country_code: country abbreviation
    year: year of data

    Returns:
    dict: country data for the specified year
    """
    logging.debug(f"Looking up {country_code}:{year}")
    data = rd.get(f"{country_code}:{year}")
    
    if data is None:
        logging.error(f"Did not find record {country_code}:{year}")
        raise HTTPException(status_code=404, detail=f"Did not find record {country_code}:{year}")

    return json.loads(data)

@app.get("/countries/{country_code}")
def get_country_all_years(country_code: str) -> list:
    """
    Returns all records for a given country across all years

    Args:
    country_code: country abbreviation

    Returns:
    list: all records for the given country
    """
    logging.debug(f"Fetching all records for country {country_code}")

    output = []
    for key in rd.keys():
        key_str = key.decode("utf-8")
        if key_str.startswith(f"{country_code}:"):
            output.append(json.loads(rd.get(key)))
    return output

@app.post("/jobs")
def create_job(job: JobInput) -> Job:
    """
    Creates a new job and adds it to the queue
    """

    logging.info(f"Received job request: country_code={job.country_code}, "f"start_year={job.start_year}, end_year={job.end_year}")
    if job.start_year > job.end_year:
        raise HTTPException(status_code=400, detail="start_year must be <= end_year")

    found = False
    for key in rd.keys():
        key_str = key.decode("utf-8")
        if key_str.startswith(f"{job.country_code}:"):
            year = int(key_str.split(":")[1])
            if job.start_year <= year <= job.end_year:
                found = True
                break
    if (found == False):
        logging.warning("No matching data for given parameters")

    if not found:
        raise HTTPException(status_code=400, detail="No matching data for given parameters")

    return add_job(job.country_code, job.start_year, job.end_year)

@app.get("/jobs")
def list_all_jobs() -> list:
    """
    Returns all job IDs
    """
    return get_job_ids()

@app.get("/jobs/{jobid}")
def get_job(jobid: str) -> Job:
    """
    Returns job info for a specific job
    """
    logging.debug(f"Fetching job {jobid}")
    job = get_job_by_id(jobid)

    if job is None:
        raise HTTPException(status_code=404, detail=f"Did not find job {jobid}")

    return job

@app.get("/results/{jobid}")
def get_results(jobid: str) -> dict:
    """
    Returns the result for given job id
    """
    logging.debug(f"Fetching job result for {jobid}")
    job = get_job_by_id(jobid)

    if job is None:
        raise HTTPException(status_code=404, detail=f"Did not find job {jobid}")

    result = get_result(jobid)
    if result is None: 
        raise HTTPException(status_code=404, detail="Job not finished")
    return result
