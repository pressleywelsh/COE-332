import json

with open('Meteorite_Landings_Simple.json', 'r') as f:
    ml_data = json.load(f)

type(ml_data)

ml_data.keys()

print(ml_data)

