import requests
import xmltodict
from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator
from math import sqrt


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
        for key in ["X", "Y", "Z", "X_DOT", "Y_DOT", "Z_DOT"]:
            if isinstance(values.get(key), dict) and "#text" in values[key]:
                values[key] = values[key]["#text"]
        return values
def timeRange(NASA: list[vectors]) -> str:
    """
    Determines the range that the ISS covers data over

    Args: 
    NASA: list of vectors

    Returns:
    time_range: string of data span
    """
    firstEpoch = NASA[0].EPOCH
    lastEpoch = NASA[len(NASA)-1].EPOCH
    time_range = (f"The data spans from {firstEpoch} to {lastEpoch}")
    return time_range

def recentEpoch(NASA: list[vectors]) -> vectors:
    """
    Determines the vector that is closest to the current UTC time

    Args: 
    NASA: list of vectors

    Returns:
    NASA[bestIndex]: vector with epoch closest to now
    """
    currentTime = datetime.now(timezone.utc)
    bestIndex = 0
    diff = abs(currentTime - datetime.strptime(NASA[0].EPOCH, "%Y-%jT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc))
    ind = 0
    for row in NASA:
        epochDate = datetime.strptime(row.EPOCH, "%Y-%jT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        difference = abs(currentTime - epochDate)
        if (difference<diff):
            bestIndex = ind
            diff = difference
        ind += 1
    return NASA[bestIndex]

def calcSpeed(row: vectors) -> float:
    """
    Computes instantaneous speed from cartesian velocity components

    Args: 
    row: one ISS vector

    Returns: 
    speed: speed found using speed equation
    """
    speed = sqrt((row.X_DOT ** 2) + (row.Y_DOT ** 2) + (row.Z_DOT **2))
    return speed

def averageSpeed (NASA: list[vectors]) -> float:
    """
    Computes average speed over the whole dataset

    Args:
    NASA: list of vectors

    Returns: 
    avg: sum of speed divided by length of list to find average
    """
    sumSpeed = 0
    for row in NASA:
        sumSpeed += calcSpeed(row)
    avg = sumSpeed/len(NASA)
    return (avg)

def main():
    xml = requests.get(f"https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    unsortedData = xml.text
    data = xmltodict.parse(unsortedData)
    rows = data["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]
    NASA = [vectors(**row) for row in rows]
    print(timeRange(NASA))
    recent = recentEpoch(NASA)
    print(f"Closest epoch to now is: {recent}")
    avgSpeed = averageSpeed(NASA)
    print(f"Average speed over data is: {avgSpeed}")
    instSpeed = calcSpeed(recent)
    print(f"Instantaneous speed closest to now: {instSpeed}")

if __name__ == '__main__':
    main()
