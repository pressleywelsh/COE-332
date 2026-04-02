from pydantic import BaseModel
import requests
import redis
import json
from fastapi import FastAPI
import csv
from typing import Optional

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

@app.get("/help")
def help():
    return {
        "routes": {
            "/data POST": "load data into Redis",
            "/data GET": "return all data",
            "/data DELETE": "delete all data",
            "/countries GET": "return all country_code:year keys",
            "/countries/{country_code}/{year} GET": "return one record"
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

    with open("world_health_data.csv", "r") as f:
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

    return {"data_loaded": count}

@app.get("/data")
def get_data() -> list:
    """
    Returns all data stored in Redis

    Returns:
    list: all country data records
    """
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
    data = rd.get(f"{country_code}:{year}")
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
    output = []
    for key in rd.keys():
        key_str = key.decode("utf-8")
        if key_str.startswith(f"{country_code}:"):
            output.append(json.loads(rd.get(key)))
    return output
