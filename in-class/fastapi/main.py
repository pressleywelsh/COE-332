from fastapi import FastAPI
import requests

app = FastAPI()

#@app.get("/")
#def root():
#    return {"message": "Hello World"}

@app.get('/{name}')
def hello_name(name: str):
    return { "message": f"Hello, {name}"}

"""
@app.get('/meteorite_landings')
def get_data():
    url = "https://raw.githubusercontent.com/TACC/coe-332-sp26/main/docs/unit02/sample-data/Meteorite_Landings.json"
    rsp = requests.get(url)
    return rsp.json
"""


def get_data():
    return [ {'id': 0, 'year': 1990, 'degrees': 5818},
             {'id': 1, 'year': 1991, 'degrees': 5725},
             {'id': 2, 'year': 1992, 'degrees': 6005},
             {'id': 3, 'year': 1993, 'degrees': 6123},
             {'id': 4, 'year': 1994, 'degrees': 6096} ]
