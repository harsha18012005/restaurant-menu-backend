from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_items(db: Session, category: str, quantity: str, limit: int):
    query = db.query(models.MenuItem)

    if category:
        query = query.filter(models.MenuItem.category == category)

    if quantity:
        query = query.filter(models.MenuItem.quantity == quantity)

    return query.limit(limit).all()


def run_scraper():
    db = SessionLocal()

    try:
        category = input("Enter category: ")
        quantity = input("Enter quantity: ") 
        limit = int(input("Enter your limit: "))

        items = fetch_items(db, category, quantity, limit)

        if not items:
            print("No data found")
            return

        for item in items:
            print({
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "price": item.price,
                "quantity": item.quantity
            })

        logger.info(
            f"Fetched {limit} items | Category: {category} | Quantity: {quantity}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    run_scraper()