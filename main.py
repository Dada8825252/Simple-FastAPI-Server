from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# In-memory database and item ID counter
items_db: Dict[int, Dict] = {}
current_id = 1

# Pydantic model for item
class Item(BaseModel):
    name: str = None
    price: float = 0.0

# GET: Fetch all items
@app.get("/items/", response_model=List[Dict])
def get_items():
    return [{"id": item_id, **item.dict()} for item_id, item in items_db.items()]

# GET: Fetch a specific item by its ID
@app.get("/items/{item_id}", response_model=Dict)
def get_item(item_id: int):
    if item_id in items_db:
        return {"id": item_id, **items_db[item_id].dict()}
    raise HTTPException(status_code=404, detail="Item not found")

# POST: Create a new item
@app.post("/items/", response_model=Dict)
def create_item(item: Item):
    global current_id
    items_db[current_id] = item
    response = {"id": current_id, **item.dict()}
    current_id += 1  # Increment the item ID counter
    return response

# PUT: Update an item by its ID
@app.put("/items/{item_id}", response_model=Dict)
def update_item(item_id: int, item: Item):
    if item_id in items_db:
        items_db[item_id] = item
        return {"id": item_id, **item.dict()}
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE: Delete an item by its ID
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    if item_id in items_db:
        del items_db[item_id]
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# To run the FastAPI app:
# uvicorn main:app --reload
