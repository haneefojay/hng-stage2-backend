#  🌍 Country Data Service (FastAPI)

This project is a FastAPI service that fetches, stores, and serves country information.  
Data is sourced from external APIs and synced into a PostgreSQL database.  
The service supports refreshing the database, listing countries, and retrieving country details.

---

## Features

| Fetches country data from external APIs | Country info + population data |
| Stores data in PostgreSQL | Uses async SQLAlchemy (`postgresql+asyncpg`) |
| Refresh database endpoint | Re-populates data without duplication |
| Get country list | Returns country name + ISO2 + ISO3 |
| Get detailed country info | Returns location, currency, population, and more |
| Proper error handling | Graceful responses with correct status codes |

---

## Tech Stack

- **FastAPI** 
- **SQLAlchemy** 
- **Postgresql**
- **Pydantic**
- **Uvicorn**
- **HTTPX**

---

## Setup Instructions

### 1 Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```
---

## 2. Create and activate a virtual environment

python -m venv venv

venv\Scripts\activate    # for Windows
or
source venv/bin/activate # for Mac/Linux

---

## 3. Install dependencies
pip install -r requirements.txt

---

## 4. Set environment variables

Create a .env file in the project root and add:

DATABASE_URL=YOUR_DB_URL

---

## 5. Run the server
uvicorn app.main:app --reload

Visit: http://127.0.0.1:8000/

---

## 🪄 Author

Name: Haneef Ojuatalyo
Email: haneefojutalayo@gmail.com

Stack: Python/FastAPI
Track: HNG Backend
