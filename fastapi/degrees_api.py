from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel


class DegreesRequest(BaseModel):
    year: int
    degrees: int

class DegreesResponse(DegreesRequest):
    id: int

app = FastAPI()

def get_data():
    return [ {'id': 0, 'year': 1990, 'degrees': 5818},
             {'id': 1, 'year': 1991, 'degrees': 5725},
             {'id': 2, 'year': 1992, 'degrees': 6005},
             {'id': 3, 'year': 1993, 'degrees': 6123},
             {'id': 4, 'year': 1994, 'degrees': 6096} ]

data = get_data()

""""
@app.get('/degrees')
def get_degrees():
    return get_data()
"""

@app.get('/degrees')
def get_degrees(start: int = 0):
    global data
    result = []
    for d in data:
        if (d["year"]>=start):
            result.append(d)
    return result


@app.get('/degrees/{id}')
def degrees_for_id(id: int):
    global data
    for i in data:
        if i["id"] == id:
            return i
    else:
        raise HTTPException(status_code=404, detail=f"Did not find id {id}")

@app.get('/degrees/{id}/degrees')
def degrees_for_id_degree(id: int):
    global data
    for i in data:
        if i["id"] == id:
            return i['degrees']
    else:
      raise HTTPException(status_code=404, detail=f"Did not find id {id}")

@app.delete('/degrees/{id}')
def delete_degrees_obj(id: int):
    global data
    for item in data:
        if item["id"] == id:
            data.remove(item)
            return {"message": f"Item {id} deleted."}
    raise HTTPException(status_code=404, detail=f"Did not find id {id}")

@app.post("/degrees")
def create_degrees(d: DegreesRequest) -> DegreesResponse:
    global data
    # get the next id
    max_id = 0
    for degrees in data:
        if degrees['id'] > max_id:
            max_id = degrees["id"]
    new_id = max_id + 1
    new_d = DegreesResponse(year=d.year, degrees=d.degrees, id=new_id)
    data[new_id] = new_d.model_dump()
    return new_d
