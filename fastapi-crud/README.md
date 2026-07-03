# FastAPI Products CRUD REST API

A production-ready, complete RESTful CRUD API for managing "Products" resources, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

## 🚀 Features

- **Full CRUD Support**: Create, Read (all & by ID with pagination), Update, and Delete operations.
- **Data Validation**: Strict Pydantic v2 schemas with field validation (`name` min length, `price` > 0).
- **Database Integration**: SQLAlchemy 2.0 with declarative mapping and SQLite backend.
- **API Testing**: Includes a complete Postman Collection v2.1.0 (`product_api_collection.json`) with embedded status code assertion test scripts.

---

## 🛠️ Project Setup & Installation

### 1. Prerequisite Checklist
Ensure you have Python 3.8+ installed on your system.

### 2. Virtual Environment Setup
It is recommended to use a virtual environment to manage project dependencies.

#### On Windows (PowerShell / Command Prompt):
```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Package Installation
Install the required packages (`fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`). You can install them directly or via `requirements.txt`:

```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic
```

Or using `requirements.txt` if available:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Application Execution

To run the application locally using Uvicorn, execute the following command from within the `fastapi-crud` directory:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- The API will be available at: `http://127.0.0.1:8000/items`
- Interactive Swagger API documentation: `http://127.0.0.1:8000/docs`
- ReDoc alternative API documentation: `http://127.0.0.1:8000/redoc`

---

## 📌 Example Usage (cURL)

### Create a Product (POST /items)

Here is an example raw `curl` statement to send a POST creation request:

#### On macOS / Linux / Bash:
```bash
curl -X POST "http://127.0.0.1:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Wireless Noise-Canceling Headphones",
           "description": "Over-ear Bluetooth headphones with 30-hour battery life.",
           "price": 199.99,
           "in_stock": true
         }'
```

#### On Windows PowerShell:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/items" `
                  -Method Post `
                  -Headers @{ "Content-Type" = "application/json" } `
                  -Body '{"name":"Wireless Noise-Canceling Headphones","description":"Over-ear Bluetooth headphones with 30-hour battery life.","price":199.99,"in_stock":true}'
```

---

## 🧪 Testing with Postman

Import the `product_api_collection.json` file directly into Postman:
1. Open Postman and click **Import**.
2. Select `product_api_collection.json`.
3. Run the collection against `http://127.0.0.1:8000` to execute automated test assertions for all 5 CRUD operations and 404 error handling.
