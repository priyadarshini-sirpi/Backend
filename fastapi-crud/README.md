# FastAPI Products CRUD REST API

A production-ready, complete RESTful CRUD API for managing "Products" resources, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

## 🚀 Features

- **Full CRUD Support**: Create, Read (all & by ID with pagination), Update, and Delete operations.
- **Advanced Querying (Phase 3)**: Multi-parameter filtering (`category`, `min_price`, `max_price`), case-insensitive partial searching (`search`), dynamic field sorting (`sort_by`, `order`), and structured pagination (`skip`, `limit`) with metadata response (`total`, `items`).
- **Data Validation**: Strict Pydantic v2 schemas with field validation (`name` min length, `price` > 0, `limit` <= 100).
- **Database Integration**: SQLAlchemy 2.0 with declarative mapping and SQLite backend.
- **API Testing**: Includes a complete Postman Collection v2.1.0 (`product_api_collection.json`) with embedded status code assertion test scripts covering all CRUD endpoints and Phase 3 query variations.

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

## 🔍 Phase 3 – Advanced Querying (`GET /items`)

The `GET /items` endpoint supports production-ready advanced querying, combining **filtering**, **searching**, **sorting**, and **pagination** inside SQLAlchemy using chaining and strict execution order.

### Execution Order
Queries are strictly executed in the following order:
1. **Filtering**: Applies exact match (`category`) and range checks (`min_price`, `max_price`) using `AND` logic.
2. **Search**: Applies case-insensitive partial matching (`ILIKE`) using `OR` logic across existing text fields (`name`, `description`).
3. **Sorting**: Orders results by the validated field (`sort_by`) and direction (`order`).
4. **Pagination**: Counts total matching records (`total`) *before* slicing the query (`skip` and `limit`).

### Supported Query Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `category` | `string` | `None` | Exact match filter by category. If no records match (or model lacks attribute), returns `200 OK` with `items: []`. |
| `min_price` | `float` | `None` | Filters records where `price >= min_price`. |
| `max_price` | `float` | `None` | Filters records where `price <= max_price`. |
| `search` | `string` | `None` | Case-insensitive partial search (`ILIKE`) automatically detecting existing text fields (`name`, `description`, `title`). |
| `sort_by` | `string` | `None` | Field to sort by. Approved values: `price`, `created_at` (falls back to `id` if timestamp is unavailable), and standard attributes. Returns `422 Unprocessable Entity` if invalid. |
| `order` | `string` | `desc` | Sort direction (`asc` or `desc`). Returns `422` if invalid. |
| `skip` | `integer` | `0` | Number of records to skip (`skip >= 0`). |
| `limit` | `integer` | `10` | Maximum records to return (`limit >= 0`, max `100`). Requesting `limit > 100` (e.g. `limit=500`) returns `422 Unprocessable Entity` via FastAPI validation. |

### Paginated Response Structure
```json
{
  "total": 42,
  "skip": 0,
  "limit": 10,
  "items": [
    {
      "name": "Wireless Mechanical Keyboard",
      "description": "Compact 75% mechanical keyboard with RGB backlighting.",
      "price": 89.99,
      "in_stock": true,
      "id": 1,
      "user_id": 1
    }
  ]
}
```

### Example URLs

- **Filter Only**:
  ```http
  GET /items?category=fiction
  GET /items?min_price=50&max_price=200
  ```
- **Search Only**:
  ```http
  GET /items?search=dragon
  ```
- **Sort Ascending**:
  ```http
  GET /items?sort_by=price&order=asc
  ```
- **Sort Descending**:
  ```http
  GET /items?sort_by=price&order=desc
  ```
- **Combined Query**:
  ```http
  GET /items?category=fiction&search=dragon&sort_by=price&order=desc&skip=0&limit=10
  ```
- **Invalid Sort Field (Expect HTTP 422)**:
  ```http
  GET /items?sort_by=salary
  ```
- **Limit Greater Than 100 (Expect HTTP 422)**:
  ```http
  GET /items?limit=500
  ```

---

## 🧪 Testing with Postman

Import the `product_api_collection.json` file directly into Postman:
1. Open Postman and click **Import**.
2. Select `product_api_collection.json`.
3. Run the collection against `http://127.0.0.1:8000` to execute automated test assertions for:
   - All 5 standard CRUD endpoints (`POST /items`, `GET /items`, `GET /items/{id}`, `PUT /items/{id}`, `DELETE /items/{id}`).
   - All Phase 3 Querying variations (filtering, searching, sorting, combined queries, and 422 validation errors).
   - 404 error handling for non-existent IDs.

