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

def main():
    xml = requests.get(f"https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    unsortedData = xml.text
    data = xmltodict.parse(unsortedData)
    rows = data["ndm"]["oem"]["body"]["segment"]["data"]["stateVector"]
    NASA = [vectors(**row) for row in rows]
    print(type(data))
    print(data.keys())
    print(len(rows))
    print(NASA[0])

if __name__ == '__main__':
    main()
