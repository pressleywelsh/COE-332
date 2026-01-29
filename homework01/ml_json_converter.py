import csv
import xmltodict
import yaml
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


def main():
    data_path = Path.cwd().parent / "Meteorite_Landings_Simple.json"
    
    with data_path.open("r") as f:
        data = json.load(f)
        
    landings = [MeteoriteLanding(**ml) for ml in data["meteorite_landings"]]
    rows = [ml.model_dump() for ml in landings]

    csv_path = Path.cwd().parent / "Meteorite_Landings.csv"

    with csv_path.open("w") as o:
        csv_dict_writer = csv.DictWriter(o, rows[0].keys())
        csv_dict_writer.writeheader()
        csv_dict_writer.writerows(rows)

    xml_path = Path.cwd().parent / "Meteorite_Landings.xml"
    xml_data = {"meteorite_landings": rows}

    with xml_path.open("w") as o:
        o.write(xmltodict.unparse(xml_data, pretty=True))

    yaml_path = Path.cwd().parent / "Meteorite_Landings.yaml"
    yaml_data = {"meteorite_landings": rows} 

    with yaml_path.open("w") as o:
        yaml.dump(yaml_data, o)


if __name__ == '__main__':
    main()
