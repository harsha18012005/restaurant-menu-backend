import requests
import logging
import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = "https://api.github.com/users"
PER_PAGE = 10
MAX_PAGES = 100
def fetch_users(page: int):
    params = {
        "per_page": PER_PAGE,
        "page": page
    }

    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code}")
            return []

        return response.json()

    except Exception as e:
        logger.error(f"Request failed: {e}")
        return []
def extract_users():
    all_users = []

    for page in range(1, MAX_PAGES + 1):
        logger.info(f"Fetching page {page}")

        users = fetch_users(page)
        if not users:
            logger.warning("No more API data")
            break

        for user in users:
            cleaned = {
                "id": user.get("id"),
                "name": user.get("login"),
                "url": user.get("html_url")
            }
            all_users.append(cleaned)

    return all_users
def fetch_menu_items(db: Session):
    try:
        return db.query(models.MenuItem).all()
    except Exception as e:
        logger.error(f"DB Error: {e}")
        return []
def extract_category_wise(items):
    category_data = {}

    for item in items:
        category = item.category or "Unknown"

        if category not in category_data:
            category_data[category] = []

        category_data[category].append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity
        })
    for category in category_data:
        category_data[category] = sorted(
            category_data[category],
            key=lambda x: x["price"]
        )

    return category_data
def save_to_json(data, filename="menu_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Data saved to {filename}")
def run_scraper():
    db = SessionLocal()

    try:
        logger.info("Starting scraper...")
        api_data = extract_users()
        logger.info(f"Extracted {len(api_data)} users from API")
        items = fetch_menu_items(db)

        if not items:
            logger.warning("No menu data found")
            return

        category_data = extract_category_wise(items)
        for category, items in category_data.items():
            print(f"\n=== {category} ===")
            for item in items:
                print(item)
        save_to_json(category_data)

        logger.info("Scraper completed successfully")

    finally:
        db.close()
if __name__ == "__main__":
    run_scraper()
