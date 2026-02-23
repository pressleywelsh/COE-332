import requests
import xmltodict
from pydantic import BaseModel, Field, model_validator


class vectors(BaseModel):
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
    firstEpoch = NASA[0].EPOCH
    lastEpoch = NASA[len(NASA)-1].EPOCH
    time_range = (f"The data spans from {firstEpoch} to {lastEpoch}")
    return time_range

def fullEpoch(NASA: list[vectors]) -> vectors:
    recentEpoch = NASA[len(NASA)-1]
    return recentEpoch

def main():
    xml = requests.get(f"https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    unsortedData = xml.text
    data = xmltodict.parse(unsortedData)
    rows = data["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]
    NASA = [vectors(**row) for row in rows]
    print(timeRange(NASA))

if __name__ == '__main__':
    main()
