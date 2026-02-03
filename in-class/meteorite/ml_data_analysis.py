#!/usr/bin/env python3
import json
from models import MeteoriteLanding, compute_average_mass, check_hemisphere


def main():

    with open('Meteorite_Landings_Simple.json', 'r') as f:
        ml_data = json.load(f)

    landings = [MeteoriteLanding(**ml) for ml in ml_data["meteorite_landings"]]

    print(compute_average_mass(landings))

    for ml in landings:
        print(check_hemisphere(ml))

if __name__ == '__main__':
    main()
