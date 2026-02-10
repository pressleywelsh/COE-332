import json
import logging
from pydantic import BaseModel, Field, model_validator
from pathlib import Path
from gcd_algorithm import great_circle_distance


class GeoLocation(BaseModel):
    lat: float
    long: float

class MeteoriteLanding(BaseModel):
    name: str
    id: int
    mass: int = Field(alias="mass (g)")
    class_name: str = Field(alias="recclass")
    location: GeoLocation

    @model_validator(mode="before")
    @classmethod
    def preprocess_inputs(cls, values):
        values["location"] = {
            "lat": values["reclat"],
            "long": values["reclong"],
        }
        return values

def check_hemisphere(ml: MeteoriteLanding) -> str:
    """
    Given a meteorite landing's location (latitude and longitude in decimal notation),
    returns which hemispheres those coordinates land in.

    Args:
        ml: A MeteoriteLanding object

    Returns:
        location: Short string listing two hemispheres.
    """
    location = ''
    if (ml.location.lat > 0):
        location = 'Northern'
    else:
        location = 'Southern'
    if (ml.location.long > 0):
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'
    return(location)

def compute_average_mass(landings: list[MeteoriteLanding]) -> float:
    """
    Iterates through a list of meteorite landing objects, adds their masses together
    and returns that sum divided by the total number or landings

    Args:
        landings: A list of meteorite landing objects

    Returns:
        result: Average value.
    """
    if (len(landings) == 0):
        logging.error("landings is empty")
        return 0
    total_mass = 0.
    for ml in landings:
        total_mass += ml.mass
    return (total_mass / len(landings))

def count_classes(landings: list[MeteoriteLanding]) -> dict[str, int]:
    """
    Counts how many meteorite landings occur in each meteorite class

    Args:
        landings: A list of MeteoriteLanding objects

    Returns:
        classes_observed: Dictionary of meteorite classes and their counts.
    """
    classes_observed = {}
    for ml in landings:
        if ml.class_name not in classes_observed:
            classes_observed[ml.class_name] = 0

        classes_observed[ml.class_name] += 1
    return(classes_observed)

def main():
    data_path = Path.cwd().parent / "Meteorite_Landings.json"

    with data_path.open("r") as f:
        data = json.load(f)

    landings = [MeteoriteLanding(**ml) for ml in data["meteorite_landings"]]
    rows = [ml.model_dump() for ml in landings]

    csv_path = Path.cwd() / "Meteorite_Landings.csv"

    with csv_path.open("w") as o:
        csv_dict_writer = csv.DictWriter(o, rows[0].keys())
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(rows)

    with csv_path.open("r") as f:
        reader = csv.DictReader(f)
        landings = [MeteoriteLanding(**row) for row in reader]

    print(compute_average_mass(landings))

    for ml in landings:
        print(check_hemisphere(ml))

    print(count_classes(landings))

    r=6371
    distance_1and2 = great_circle_distance(
            landings[0].location.lat, landings[0].location.long,
            landings[1].location.lat, landings[1].location.long, r)
    print("distance between landing 1 and 2: ", distance_1and2)

    distance_3and4 = great_circle_distance(
            landings[2].location.lat, landings[2].location.long,
            landings[3].location.lat, landings[3].location.long, r)
    print("distance between landing 3 and 4: ", distance_3and4)

    distance_5and6 = great_circle_distance(
            landings[4].location.lat, landings[4].location.long,
            landings[5].location.lat, landings[5].location.long, r)
    print("distance between landing 5 and 6: ", distance_5and6)

if __name__ == '__main__':
    main()
