from fastapi import FastAPI

app = FastAPI()

def get_data():
    return [ {'id': 0, 'year': 1990, 'degrees': 5818},
             {'id': 1, 'year': 1991, 'degrees': 5725},
             {'id': 2, 'year': 1992, 'degrees': 6005},
             {'id': 3, 'year': 1993, 'degrees': 6123},
             {'id': 4, 'year': 1994, 'degrees': 6096} ]

""""
@app.get("/degrees")
def get_degrees():
    return get_data()
"""

@app.get("/degrees")
def get_degrees(start: int = 0):
    data = get_data()
    result = []
    for d in data:
        if (d["year"]>=start):
            result.append(d)
    return result


@app.get('/degrees/{id}')
def degrees_for_id(id: int):
    data = get_data()
    for i in data:
        if i["id"] == id:
            return i
    return {"message": f"Error: did not find {id}"}
        
@app.get('/degrees/{id}/degrees')
def degrees_for_id_degree(id: int):
    data = get_data()
    for i in data:
        if i["id"] == id:
            return i['degrees']
        