import requests
import xmltodict
import logging
from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator
from math import sqrt
from fastapi import FastAPI, HTTPException


logging.basicConfig(level=logging.INFO)

class vectors(BaseModel):
    """
    Pydantic model of an ISS state vector

    Includes: 
    - EPOCH: time stamp
    - X, Y, Z: cartesian position vector
    - X_DOT, Y_DOT, Z_DOT: cartesian velocity vector

    It also cleans the XML data of text
    """
    EPOCH: str
    X: float
    Y: float
    Z: float
    X_DOT: float
    Y_DOT: float
    Z_DOT: float
    @model_validator(mode="before")
    @classmethod
    def cleanUnits(cls, values):
        logging.debug("Cleaning XML data")
        for key in ["X", "Y", "Z", "X_DOT", "Y_DOT", "Z_DOT"]:
            if isinstance(values.get(key), dict) and "#text" in values[key]:
                values[key] = values[key]["#text"]
        return values

app = FastAPI()

def get_data():
    """
    Fills dataset using requests
    """
    logging.debug("Using requests to get data")
    xml = requests.get(f"https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    unsortedData = xml.text
    data = xmltodict.parse(unsortedData)
    rows = data["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]
    NASA = [vectors(**row) for row in rows]
    return NASA

data = get_data()

def calcSpeed(row: vectors) -> float:
    """
    Computes instantaneous speed from cartesian velocity components

    Args: 
    row: one ISS vector

    Returns: 
    speed: speed found using speed equation
    """
    logging.debug(f"Calculating speed for epoch {row.EPOCH}")
    speed = sqrt((row.X_DOT ** 2) + (row.Y_DOT ** 2) + (row.Z_DOT **2))
    return speed

@app.get('/epochs')
def epochRange(limit: int = None, offset: int = 0):
    ind = 0
    result = []
    logging.debug("Sorting through vectors to find ones in given set")
    for d in data:
        if (ind>=offset):
            result.append(d)
            lim+=1
        ind+=1
        if (len(result) == limit):
            return result
    return result

@app.get('/epochs/{EPOCH}')
def get_epoch(EPOCH: str):
    for d in data:
        if d.EPOCH == EPOCH:
            return d
    raise HTTPException(status_code=404, detail=f"Did not find epoch {EPOCH}")

@app.get('/epochs/{EPOCH}/speed')
def get_speed(EPOCH: str):
    for d in data: 
        if d.EPOCH == EPOCH:
            speed = calcSpeed(d)
            return speed
    raise HTTPException(status_code=404, detail=f"Did not find epoch {EPOCH}")
            
@app.get('/now')
def recentEpoch() -> vectors:
    """
    Determines the vector that is closest to the current UTC time

    Returns:
    data[bestIndex]: state vector with epoch closest to current time
    """
    logging.debug("Finding epoch closest to current time")
    currentTime = datetime.now(timezone.utc)
    bestIndex = 0
    diff = abs(currentTime - datetime.strptime(data[0].EPOCH, "%Y-%jT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc))
    ind = 0
    for d in data:
        epochDate = datetime.strptime(d.EPOCH, "%Y-%jT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        difference = abs(currentTime - epochDate)
        if (difference<diff):
            bestIndex = ind
            diff = difference
        ind += 1
    logging.debug(f"Closest epoch found at index {bestIndex}")
    return data[bestIndex]
