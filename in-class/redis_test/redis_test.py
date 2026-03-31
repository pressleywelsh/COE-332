import redis
import json 
from pydantic import BaseModel


class MeteoriteLanding(BaseModel):
    name: str
    id: int
    class_name: str
    mass: int
    lat: float
    long: float

def main():
    rd=redis.Redis(host='127.0.0.1', port=6379, db=10)
    print(type(rd))

    rd.set("test_key", "hello")
    print(rd.get("test_key"))
    print(rd.get("test_key").decode("utf-8"))

    with open('Meteorite_Landings.json', 'r') as f:
        ml_data = json.load(f)

    landings = [MeteoriteLanding(**ml) for ml in ml_data["meteorite_landings"]]
    for landing in landings:
        key = f"meteor:{landing.id}"
        rd.set(key, json.dumps(landing.model_dump()))

if __name__ == "__main__":
    main()
