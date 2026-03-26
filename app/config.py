import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = "mysql+pymysql://root:harsha@localhost:3306/menu"

# Scraper API (given in assignment)
BASE_API_URL = os.getenv(
    "BASE_API_URL",
    "https://api.github.com/users"
)

# Scraping config
PER_PAGE = int(os.getenv("PER_PAGE", 10))
MAX_PAGES = int(os.getenv("MAX_PAGES", 100))