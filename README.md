# Restaurant Menu API

## Project Overview

This project is a FastAPI-based web application for managing restaurant menu items. It provides CRUD (Create, Read, Update, Delete) operations for menu items stored in a MySQL database. The application also includes a scraper component that fetches data from an external API (GitHub users API in this case, though it can be adapted for menu data). The API endpoints are available under `/items` for menu operations.

## Features

1. **Convert cURL Requests to Python Code**: All API interactions can be performed using Python requests library instead of cURL.
2. **Poetry for Package Management**: Uses Poetry for dependency management and virtual environment handling.
3. **Data Extraction and Processing**: The scraper extracts data from external APIs (GitHub users) and processes it for storage.
4. **Database Storage**: Data is stored in a MySQL database using SQLAlchemy ORM, including both menu items and scraped user data.
5. **FastAPI Application with CRUD Operations**: RESTful API endpoints for creating, reading, updating, and deleting menu items.

## Setup Instructions

### Python Version Required
- Python 3.8 or higher

### How to Install Poetry
If you don't have Poetry installed, install it first:
```
curl -sSL https://install.python-poetry.org | python3 -
```
Or follow the official installation guide at https://python-poetry.org/docs/#installation

### How to Set Up the Project with Poetry
1. Open a terminal in the project root directory (`c:\Restaurant`).
2. Install dependencies and create virtual environment:
   ```
   poetry install
   ```
3. Activate the Poetry shell:
   ```
   poetry shell
   ```

## Database Setup

The application uses MySQL as the database. The database connection is configured in `app/config.py` with the URL: `mysql+pymysql://root:harsha@localhost:3306/menu`.

- Ensure MySQL is installed and running on your system.
- Create a database named `menu` in MySQL.
- The tables are automatically created when the application starts via `Base.metadata.create_all(bind=engine)` in `app/main.py`.

## Configuration

Environment variables are loaded from a `.env` file in the project root. The current configuration includes:

- `DATABASE_URL`: MySQL connection string
- `BASE_API_URL`: API URL for scraping (defaults to GitHub API)
- `PER_PAGE`: Number of items per page for API requests
- `MAX_PAGES`: Maximum pages to fetch from API

You can modify these values in the `.env` file as needed.

## Running the Project End-to-End

### 1. Set Up Environment
- Install Poetry and set up the project as described in Setup Instructions.
- Ensure MySQL is running and the database is created.

### 2. Run the Scraper (Data Extraction, Processing, and Storage)
The scraper loads initial menu data from `menu_data.json` into the database, fetches data from the GitHub API (up to 100 pages with 10 items per page), stores the scraped user data in the database, processes existing menu data, and saves processed data back to JSON:
```
poetry run python app/scraper.py
```

### 3. Start the FastAPI Server (CRUD Operations)
```
poetry run uvicorn app.main:app --reload
```

### 4. Access API Documentation
Once the server is running, visit:
http://127.0.0.1:8000/docs

This will open the interactive Swagger UI for testing the API endpoints.

## API Examples

Here are sample requests to interact with the API, shown both as cURL commands and Python code using the requests library.

### Create Menu Items

**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/items" \
-H "Content-Type: application/json" \
-d '[
  {
    "name": "Margherita Pizza",
    "category": "Pizza",
    "price": 12.99,
    "quantity": "1 large"
  },
  {
    "name": "Caesar Salad",
    "category": "Salad",
    "price": 8.50,
    "quantity": "1 serving"
  }
]'
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/items"
data = [
    {
        "name": "Margherita Pizza",
        "category": "Pizza",
        "price": 12.99,
        "quantity": "1 large"
    },
    {
        "name": "Caesar Salad",
        "category": "Salad",
        "price": 8.50,
        "quantity": "1 serving"
    }
]
response = requests.post(url, json=data)
print(response.json())
```

### Get All Menu Items

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/items" \
-H "accept: application/json"
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/items"
response = requests.get(url)
print(response.json())
```

### Get a Specific Menu Item

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/items/1" \
-H "accept: application/json"
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/items/1"
response = requests.get(url)
print(response.json())
```

### Update a Menu Item

**cURL:**
```bash
curl -X PUT "http://127.0.0.1:8000/items/1" \
-H "Content-Type: application/json" \
-d '{
  "name": "Updated Pizza",
  "category": "Pizza",
  "price": 14.99,
  "quantity": "1 large"
}'
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/items/1"
data = {
    "name": "Updated Pizza",
    "category": "Pizza",
    "price": 14.99,
    "quantity": "1 large"
}
response = requests.put(url, json=data)
print(response.json())
```

### Delete a Menu Item

**cURL:**
```bash
curl -X DELETE "http://127.0.0.1:8000/items/1"
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/items/1"
response = requests.delete(url)
print(response.status_code)
```

### Filter Menu Items

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/items/filter?name=Pizza&category=Pizza&max_price=20" \
-H "accept: application/json"
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/items/filter"
params = {
    "name": "Pizza",
    "category": "Pizza",
    "max_price": 20
}
response = requests.get(url, params=params)
print(response.json())
```