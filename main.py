from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Demo",
    description="A simple FastAPI demo application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Item(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True
    created_at: Optional[datetime] = None

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None

# In-memory storage (in a real app, you'd use a database)
items_db = []

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Demo!", "version": "1.0.0"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Get all items
@app.get("/items", response_model=List[Item])
async def get_items():
    return items_db

# Get item by ID
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = next((item for item in items_db if item["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Create new item
@app.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    new_item = Item(
        id=str(uuid.uuid4()),
        name=item.name,
        description=item.description,
        price=item.price,
        is_available=item.is_available,
        created_at=datetime.now()
    )
    items_db.append(new_item.dict())
    return new_item

# Update item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemUpdate):
    item_index = next((i for i, item in enumerate(items_db) if item["id"] == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    for field, value in item_update.dict(exclude_unset=True).items():
        items_db[item_index][field] = value
    
    return items_db[item_index]

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    item_index = next((i for i, item in enumerate(items_db) if item["id"] == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items_db.pop(item_index)
    return {"message": "Item deleted successfully", "deleted_item": deleted_item}

# Search items
@app.get("/items/search/", response_model=List[Item])
async def search_items(q: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    filtered_items = items_db
    
    if q:
        filtered_items = [item for item in filtered_items if q.lower() in item["name"].lower()]
    
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] >= min_price]
    
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] <= max_price]
    
    return filtered_items

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
