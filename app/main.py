from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import schemas, crud
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CREATE
@app.post("/menu")
def create(items: List[schemas.MenuItemCreate], db: Session = Depends(get_db)):
    result = []
    for item in items:
        result.append(crud.create_item(db, item))
    return result

# READ ALL
@app.get("/menu", response_model=list[schemas.MenuItemResponse])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_items(db, skip, limit)

# READ ONE
@app.get("/menu/{id}", response_model=schemas.MenuItemResponse)
def get_one(id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# UPDATE
@app.put("/menu/{id}", response_model=schemas.MenuItemResponse)
def update(id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    updated = crud.update_item(db, id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

# DELETE
@app.delete("/menu/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_item(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}



@app.get("/menu/filter", response_model=list[schemas.MenuItemResponse])
def filter_items(
    id: Optional[int] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    return crud.filter_items(db, id, name, category, max_price)