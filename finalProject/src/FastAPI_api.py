from pydantic import BaseModel
import requests
import redis
import json
from fastapi import FastAPI, HTTPException
import csv
import logging
import os
from typing import Optional
from jobs import rdb, add_job, get_job_by_id, get_job_ids, Job, get_result
from fastapi.responses import FileResponse


logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

def get_redis_client():
    return redis.Redis(host=os.environ.get("REDIS_IP", "redis-db"), port=6379, db=0)

rd = get_redis_client()

VALID_YEARS = {2015, 2016, 2017, 2018, 2019}

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
            "/results/{jobid} GET": "get job result",
            "/download/{jid} GET": "download output.png for a completed job",
            "/data/stats GET": "return summary statistics for the dataset"
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
            if int(row["year"]) not in VALID_YEARS:
                continue

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

@app.get("/data/stats")
def get_stats() -> dict:
    """
    Returns summary statistics for the data in Redis

    Returns:
    dict: formatted summary statistics for the dataset
    """
    logging.info("Computing dataset statistics")

    records = []
    for key in rd.keys():
        records.append(countryData(**json.loads(rd.get(key))))

    if len(records) == 0:
        raise HTTPException(status_code=404, detail="No data loaded. POST /data first.")

    life_expects = []
    health_exps = []
    infant_morts = []
    maternal_morts = []
    neonatal_morts = []
    under5_morts = []
    hiv_prevs = []
    undernourishments = []

    for record in records:
        if record.life_expect is not None:
            life_expects.append(record.life_expect)
        if record.health_exp is not None:
            health_exps.append(record.health_exp)
        if record.infant_mortality is not None:
            infant_morts.append(record.infant_mortality)
        if record.maternal_mortality is not None:
            maternal_morts.append(record.maternal_mortality)
        if record.neonatal_mortality is not None:
            neonatal_morts.append(record.neonatal_mortality)
        if record.under_5_mortality is not None:
            under5_morts.append(record.under_5_mortality)
        if record.prev_hiv is not None:
            hiv_prevs.append(record.prev_hiv)
        if record.prev_undernourishment is not None:
            undernourishments.append(record.prev_undernourishment)

    mean_life = sum(life_expects) / len(life_expects)
    mean_exp = sum(health_exps) / len(health_exps)
    mean_infant = sum(infant_morts) / len(infant_morts)
    mean_mat = sum(maternal_morts) / len(maternal_morts)
    mean_neo = sum(neonatal_morts) / len(neonatal_morts)
    mean_u5 = sum(under5_morts) / len(under5_morts)
    mean_hiv = sum(hiv_prevs) / len(hiv_prevs)
    mean_undr = sum(undernourishments) / len(undernourishments)

    std_life = (sum((value - mean_life) ** 2 for value in life_expects) / len(life_expects)) ** 0.5
    std_exp = (sum((value - mean_exp) ** 2 for value in health_exps) / len(health_exps)) ** 0.5

    max_life_rec = records[0]
    min_life_rec = records[0]
    max_exp_rec = records[0]
    min_exp_rec = records[0]
    max_mat_rec = records[0]
    min_mat_rec = records[0]
    max_hiv_rec = records[0]

    for record in records:

        if record.life_expect is not None:
            if max_life_rec.life_expect is None or record.life_expect > max_life_rec.life_expect:
                max_life_rec = record
            if min_life_rec.life_expect is None or record.life_expect < min_life_rec.life_expect:
                min_life_rec = record

        if record.health_exp is not None:
            if max_exp_rec.health_exp is None or record.health_exp > max_exp_rec.health_exp:
                max_exp_rec = record
            if min_exp_rec.health_exp is None or record.health_exp < min_exp_rec.health_exp:
                min_exp_rec = record

        if record.maternal_mortality is not None:
            if max_mat_rec.maternal_mortality is None or record.maternal_mortality > max_mat_rec.maternal_mortality:
                max_mat_rec = record
            if min_mat_rec.maternal_mortality is None or record.maternal_mortality < min_mat_rec.maternal_mortality:
                min_mat_rec = record

        if record.prev_hiv is not None:
            if max_hiv_rec.prev_hiv is None or record.prev_hiv > max_hiv_rec.prev_hiv:
                max_hiv_rec = record

    life_2015 = []
    life_2019 = []

    for record in records:
        if record.year == 2015 and record.life_expect is not None:
            life_2015.append(record.life_expect)
        if record.year == 2019 and record.life_expect is not None:
            life_2019.append(record.life_expect)

    avg_2015 = sum(life_2015) / len(life_2015)
    avg_2019 = sum(life_2019) / len(life_2019)
    le_change = avg_2019 - avg_2015

    by_country = {}
    for record in records:
        if record.country_code not in by_country:
            by_country[record.country_code] = []
        by_country[record.country_code].append(record)

    improved = 0
    for country_code in by_country:
        country_records = sorted(by_country[country_code], key=lambda record: record.year)

        if len(country_records) > 1:
            first = country_records[0]
            last = country_records[-1]

            if first.life_expect is not None and last.life_expect is not None:
                if last.life_expect > first.life_expect:
                    improved += 1

    lines = [
            "GLOBAL HEALTH DATASET — KEY STATISTICS (2015-2019)",

        "DATASET OVERVIEW",
        f"Total records: {len(records)}",
        f"Countries: {len(by_country)}",

        "LIFE EXPECTANCY",
        f"Global mean: {mean_life:.2f} years",
        f"Standard deviation: {std_life:.2f} years",
        f"Highest: {max_life_rec.life_expect:.2f} yrs — {max_life_rec.country} ({max_life_rec.year})",
        f"Lowest: {min_life_rec.life_expect:.2f} yrs — {min_life_rec.country} ({min_life_rec.year})",
        f"Change 2015 to 2019: {le_change:+.2f} years",
        f"Countries that improved: {improved} / {len(by_country)}",

        "HEALTH EXPENDITURE (% of GDP)",
        f"Global mean: {mean_exp:.2f}%",
        f"Standard deviation: {std_exp:.2f}%",
        f"Highest: {max_exp_rec.health_exp:.2f}% — {max_exp_rec.country} ({max_exp_rec.year})",
        f"Lowest: {min_exp_rec.health_exp:.2f}% — {min_exp_rec.country} ({min_exp_rec.year})",

        "MORTALITY INDICATORS",
        f"Mean infant mortality: {mean_infant:.2f} per 1,000 births",
        f"Mean maternal mortality: {mean_mat:.2f} per 100,000 births",
        f"Highest maternal mortality: {max_mat_rec.maternal_mortality:.2f} — {max_mat_rec.country} ({max_mat_rec.year})",
        f"Lowest maternal mortality: {min_mat_rec.maternal_mortality:.2f} — {min_mat_rec.country} ({min_mat_rec.year})",
        f"Mean under-5 mortality: {mean_u5:.2f} per 1,000",
        f"Mean neonatal mortality: {mean_neo:.2f} per 1,000",

        "HIV & UNDERNOURISHMENT",
        f"Mean HIV prevalence: {mean_hiv:.2f}% of adults 15-49",
        f"Highest HIV prevalence: {max_hiv_rec.prev_hiv:.2f}% — {max_hiv_rec.country} ({max_hiv_rec.year})",
        f"Mean undernourishment: {mean_undr:.2f}% of population"
        ]

    return { "stats": " | ".join(lines)}

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
    if year not in VALID_YEARS:
        raise HTTPException(status_code=400, detail=f"Invalid year. Valid years are {sorted(VALID_YEARS)}")

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
    if year not in VALID_YEARS:
        raise HTTPException(status_code=400, detail=f"Invalid year. Valid years are {sorted(VALID_YEARS)}")

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
    
    if len(output) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Country code '{country_code}' not found"
        )

    return output

@app.post("/jobs")
def create_job(job: JobInput) -> Job:
    """
    Creates a new job and adds it to the queue
    """

    logging.info(f"Received job request: country_code={job.country_code}, "f"start_year={job.start_year}, end_year={job.end_year}")
    if job.start_year not in VALID_YEARS or job.end_year not in VALID_YEARS:
        raise HTTPException(status_code=400, detail=f"start_year and end_year must be valid years: {sorted(VALID_YEARS)}")

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

@app.get('/download/{jid}')
def download(jid: str):
    """
    Download the plot image for a completed job

    Returns:
        FileResponse: PNG image file for the requested job
    """
    path = f'/app/{jid}.png'

    img = rdb.hget(f"{jid}:image", "data")

    if img is None:
        raise HTTPException(status_code=404, detail=f"No image found for job {jid}")

    with open(path, 'wb') as f:
        f.write(img)

    return FileResponse(path, media_type='image/png', filename=f'{jid}.png')
