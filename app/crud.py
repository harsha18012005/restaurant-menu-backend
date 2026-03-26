from sqlalchemy.orm import Session
from app import models, schemas

def create_item(db: Session, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip=0, limit=10):
    return db.query(models.MenuItem).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()

def update_item(db: Session, item_id: int, item: schemas.MenuItemCreate):
    db_item = get_item(db, item_id)
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def filter_items(db: Session, name=None, category=None, max_price=None):
    query = db.query(models.MenuItem)

    if name:
        query = query.filter(models.MenuItem.name.contains(name))
    if category:
        query = query.filter(models.MenuItem.category.contains(category))
    if max_price:
        query = query.filter(models.MenuItem.price <= max_price)

    return query.all()