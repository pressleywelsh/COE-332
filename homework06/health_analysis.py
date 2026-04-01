from pydantic import BaseModel
import requests
import redis
import json
from fastapi import FastAPI

app = FastAPI()

def get_redis_client():
    return redis.Redis(host='127.0.0.1', port=6379, db=0)

rd = get_redis_client()

class countryData(BaseModel):
    country: str
    country_code: str
    year: int
    health_exp: float
    life_expect: float
    maternal_mortality: int
    infant_mortality: float
    neonatal_mortality: float
    under_5_mortality: float
    prev_hiv: float
    inci_tuberc: float
    prev_undernourishment: float

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
    response = requests.get("https://www.kaggle.com/datasets/bushraqurban/world-health-indicators-dataset")
    data = response.json()

    count = 0
    for row in data:
        record = CountryData(**row)
        rd.set(f"{record.country_code}:{record.year}", record.model_dump_json())
        count += 1

    return {"data_loaded": count}

@app.get("/data")
def get_data() -> list:
    output = []
    for key in rd.keys():
        output.append(json.loads(rd.get(key)))
    return output

@app.delete("/data")
def delete_data() -> dict:
    keys = rd.keys()
    for key in keys:
        rd.delete(key)
    return {"data_deleted": len(keys)}

@app.get("/countries")
def get_countries() -> list:
    output = []
    for key in rd.keys():
        output.append(key.decode("utf-8"))
    return output

@app.get("/countries/{country_code}/{year}")
def get_country(country_code: str, year: int) -> dict:
    data = rd.get(f"{country_code}:{year}")
    return json.loads(data)

@app.get("/countries/{country_code}")
def get_country_all_years(country_code: str) -> list:
    output = []
    for key in rd.keys():
        key_str = key.decode("utf-8")
        if key_str.startswith(f"{country_code}:"):
            output.append(json.loads(rd.get(key)))
    return output
