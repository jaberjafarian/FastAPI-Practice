from fastapi import FastAPI
import random

app = FastAPI()

names_List = [
    {"id":1 , "name": "hassan"},
    {"id":2 , "name": "mamad"},
    {"id":3 , "name": "jaber"},
    {"id":4 , "name": "rasoul"},
    {"id":5 , "name": "zahra"},
    {"id":6 , "name": "fatme"}
    ]

@app.get("/names")
def index() :
    return names_List

@app.get("/names/{name_id}")
def retreive_name_id(name_id: int):
    for name in names_List:
        if name["id"] == name_id:
            return name
    return {"detail" : "name not found"}

@app.post("/names")
def post_name(name : str):
    name_obj = {"id": random.randint(7,100), "name":name }
    names_List.append(name_obj)
    return name
