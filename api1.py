# Creating a simple inventory management system API using FastAPI

import uvicorn 
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

inventory = {
    1 : {
        'name': 'Milk',
        'price': 50,
        'brand': 'Sudha'
    }
}

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    # Optional makes the parameter optional
    # and (= None) sets the default to None 

# Endpoint/Path Parameters
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(..., description="The ID of Item you want to view", gt=0, lt=10)):
    return inventory[item_id]

# Query Parameters
@app.get("/get-by-name")
def get__item(name: Optional[str]):
    for item_id in inventory:
        if inventory[item_id]['name']==name:
            return inventory[item_id]
    return {"Data": "Not found"}

# Request Body and POST Method
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"error": "item already in inventory"}
    inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    # inventory[item_id] = item
    return inventory[item_id]

# PUT Method
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        return {"error": "Item not in Inventory"}
    inventory[item_id].update(item)
    return inventory[item_id]
    
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)