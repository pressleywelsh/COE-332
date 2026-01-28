import json
from pydantic import BaseModel
from pathlib import Path


class MeteoriteLanding(BaseModel):
    name: str
    id: int
    class_name: str
    mass: int
    lat: float
    long: float

def compute_average_mass(landings: list[MeteoriteLanding]) -> float:
    total_mass = 0.
    for ml in landings:
        total_mass += ml.mass
    return (total_mass / len(landings))

def check_hemisphere(ml: MeteoriteLanding) -> str:
    location = ''
    if (ml.lat > 0):
        location = 'Northern'
    else:
        location = 'Southern'
    if (ml.long > 0):
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'
    return(location)


def main():
    data_path = Path.cwd().parent / "Meteorite_Landings_Simple.json"
    
    with data_path.open("r") as f:
        ml_data = json.load(f)
    
    landings = [MeteoriteLanding(**ml) for ml in ml_data["meteorite_landings"]]

    print(compute_average_mass(landings))
    
    for ml in landings: 
            print(check_hemisphere(ml))
if __name__ == '__main__':
    main()
