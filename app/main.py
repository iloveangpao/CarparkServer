from typing import Union

from fastapi import FastAPI

from app.ura import URA

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/carparkInfo/{requirement}")

async def carpark(requirement):
    uraGetter = URA()
    getter = getattr(uraGetter, requirement)
    result = getter()
    return {requirement : result}

@app.get("/items/{item_id}")

def read_item(item_id : int , q: Union[str,None] = None):
    return {"item_id": item_id, "q": q}

