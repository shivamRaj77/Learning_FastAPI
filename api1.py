# Creating a simple inventory management system API using FastAPI

import uvicorn 
from fastapi import FastAPI, Path, Query, HTTPException, status
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

# without this class the update_item function can update only specific variables only
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


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
    raise HTTPException(status_code=404, detail="Item not found!")

# Request Body and POST Method
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: UpdateItem):
    if item_id in inventory:
        raise HTTPException(status_code=404, detail="Item already in Inventory.")
    inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    # inventory[item_id] = item
    return inventory[item_id]

# PUT Method
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found!")
    
    if item.name != None:
        inventory[item_id]['name'] = item.name
    if item.price != None:
        inventory[item_id]['price'] = item.price
    if item.brand != None:
        inventory[item_id]['brand'] = item.brand

    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0, lt=10)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found!")
    del inventory[item_id]
    return {"Success": "Item removed"}
    
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)