from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import schemas, crud
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Bad request", "errors": exc.errors()},
    )

# CREATE
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create(items: List[schemas.MenuItemCreate], db: Session = Depends(get_db)):
    logger.info(f"Creating {len(items)} items")
    try:
        result = []
        for item in items:
            result.append(crud.create_item(db, item))
        logger.info("Items created successfully")
        return result
    except Exception as e:
        logger.error(f"Error creating items: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# READ ALL
@app.get("/items", response_model=list[schemas.MenuItemResponse])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Fetching all items with skip={skip}, limit={limit}")
    try:
        items = crud.get_items(db, skip, limit)
        logger.info(f"Returned {len(items)} items")
        return items
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# READ ONE
@app.get("/items/{id}", response_model=schemas.MenuItemResponse)
def get_one(id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching item with id={id}")
    item = crud.get_item(db, id)
    if not item:
        logger.warning(f"Item with id={id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.info(f"Returned item with id={id}")
    return item

# UPDATE
@app.put("/items/{id}", response_model=schemas.MenuItemResponse)
def update(id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    logger.info(f"Updating item with id={id}")
    try:
        updated = crud.update_item(db, id, item)
        if not updated:
            logger.warning(f"Item with id={id} not found for update")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        logger.info(f"Item with id={id} updated successfully")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item {id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# DELETE
@app.delete("/items/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting item with id={id}")
    try:
        deleted = crud.delete_item(db, id)
        if not deleted:
            logger.warning(f"Item with id={id} not found for deletion")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        logger.info(f"Item with id={id} deleted successfully")
        return {"message": "Deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item {id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# FILTER
@app.get("/items/filter", response_model=list[schemas.MenuItemResponse])
def filter_items(
    name: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    logger.info(f"Filtering items with name={name}, category={category}, max_price={max_price}")
    try:
        items = crud.filter_items(db, name, category, max_price)
        logger.info(f"Returned {len(items)} filtered items")
        return items
    except Exception as e:
        logger.error(f"Error filtering items: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")