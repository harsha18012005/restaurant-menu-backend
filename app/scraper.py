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
<<<<<<< HEAD


# -----------------------------
# 2.5 STORE USERS IN DB
# -----------------------------
def store_users_in_db(db: Session, users):
    from app import crud, schemas

    for user_data in users:
        # Check if exists by id
        existing = db.query(models.User).filter(models.User.id == user_data["id"]).first()
        if not existing:
            user = schemas.UserCreate(
                name=user_data["name"],
                url=user_data["url"]
            )
            crud.create_user(db, user)
            logger.info(f"Stored user: {user_data['name']}")
        else:
            logger.info(f"User already exists: {user_data['name']}")


# -----------------------------
# 3. DATABASE FETCH (YOUR PROJECT)
# -----------------------------
=======
>>>>>>> de4274a8b13cee6a858373fabcdef0b9c78aa36b
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
<<<<<<< HEAD


# -----------------------------
# 6. LOAD DATA FROM JSON TO DB
# -----------------------------
def load_data_from_json(db: Session, filename="menu_data.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        from app import crud, schemas

        for category, items in data.items():
            for item in items:
                # Check if exists
                existing = db.query(models.MenuItem).filter(models.MenuItem.name == item["name"]).first()
                if not existing:
                    menu_item = schemas.MenuItemCreate(
                        name=item["name"],
                        category=category,
                        price=item["price"],
                        quantity=item["quantity"]
                    )
                    crud.create_item(db, menu_item)
                    logger.info(f"Added: {item['name']}")
                else:
                    logger.info(f"Skipped (exists): {item['name']}")

        logger.info("Data loaded from JSON to database")

    except Exception as e:
        logger.error(f"Error loading data: {e}")


# -----------------------------
# 6. SAVE TO JSON
# -----------------------------
=======
>>>>>>> de4274a8b13cee6a858373fabcdef0b9c78aa36b
def save_to_json(data, filename="menu_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Data saved to {filename}")
def run_scraper():
    db = SessionLocal()

    try:
        logger.info("Starting scraper...")
<<<<<<< HEAD

        # 🔹 Load initial data from JSON to DB
        load_data_from_json(db)

        # 🔹 API extraction (assignment)
        api_data = extract_users()
        logger.info(f"Extracted {len(api_data)} users from API")

        # 🔹 Store scraped data in DB
        store_users_in_db(db, api_data)

        # 🔹 DB extraction (your project)
=======
        api_data = extract_users()
        logger.info(f"Extracted {len(api_data)} users from API")
>>>>>>> de4274a8b13cee6a858373fabcdef0b9c78aa36b
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
