import json
import logging
import csv
from pydantic import BaseModel, Field, model_validator
from pathlib import Path
from gcd_algorithm import great_circle_distance


logging.basicConfig(level=logging.DEBUG)

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
    logging.debug(f"Checking hemisphere of coordinate: {ml.location}")
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
    logging.debug("compute average mass function implemented")
    if (len(landings) == 0):
        logging.error("landings is empty")
        return 0
    total_mass = 0.
    for ml in landings:
        total_mass += ml.mass
        if ml.mass == 0:
            logging.warning(f"Meteorite with zero mass found: {ml.name}")
    logging.debug(f"average mass computed of: {total_mass/len(landings)}")
    return (total_mass / len(landings))

def count_classes(landings: list[MeteoriteLanding]) -> dict[str, int]:
    """
    Counts how many meteorite landings occur in each meteorite class

    Args:
        landings: A list of MeteoriteLanding objects

    Returns:
        classes_observed: Dictionary of meteorite classes and their counts.
    """
    logging.debug(f"Counting classes of {len(landings)} landings")
    classes_observed = {}
    for ml in landings:
        if ml.class_name not in classes_observed:
            classes_observed[ml.class_name] = 0
            logging.debug(f"New class of {ml.class_name} observed")

        classes_observed[ml.class_name] += 1
    logging.debug(f"{len(classes_observed)} classes observed")
    return(classes_observed)

def main():
    data = {}
    data_path = Path.cwd().parent / "Meteorite_Landings.json"

    with data_path.open("r") as f:
        data = json.load(f)

    landings = [MeteoriteLanding(**ml) for ml in data["meteorite_landings"]]
    rows = data["meteorite_landings"]

    csv_path = Path.cwd() / "Meteorite_Landings.csv"

    with csv_path.open("w") as o:
        csv_dict_writer = csv.DictWriter(o, rows[0].keys())
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(rows)

    logging.debug("csv file successfully written")

    with csv_path.open("r") as f:
        reader = csv.DictReader(f)
        landings = [MeteoriteLanding(**row) for row in reader]

    logging.debug("data successfully loaded")

    if len(landings) == 0:
        logging.error("No data loaded, can not perform calculations and analysis")
        return 0
    if (len(landings)<4):
        logging.warning(f"Not enough landings to produce accurately representative data. Only {len(landings)} landings recorded.")

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

    logging.debug("all calculations successfully completed")

if __name__ == '__main__':
    main()
