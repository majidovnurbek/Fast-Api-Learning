from fastapi import FastAPI
from models import Item

app = FastAPI()

@app.get("/item/")
async def create_item(item:Item):
    return {"item": item}


@app.put("/item/{item_id}")
async def put_item(item_id:int,item:Item,q:str |None=None):
    result={"item":item,**item.dict()}
    if q:
        result.update({"q":q})
    return result
