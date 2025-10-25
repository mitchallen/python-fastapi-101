# FastAPI Demo Project

A simple FastAPI demo application showcasing basic CRUD operations and API features.

## Quick Start

Get up and running in seconds with a single command:

```bash
make up
```

This will:
- Set up a Python virtual environment
- Install all dependencies
- Start the FastAPI server in development mode
- Handle any port conflicts automatically

Once running, visit:
- **API Documentation**: http://localhost:8000/docs
- **API Endpoint**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

To stop the server, press `Ctrl+C` or run `make stop`.

## Usage Commands

- `make up` - One command to set up and run everything
- `make stop` - Stop the running server
- `make help` - Show all available commands
- `make clean` - Clean up and start fresh

## Features

- **RESTful API** with FastAPI framework
- **Pydantic models** for data validation
- **CRUD operations** for items management
- **Search functionality** with filters
- **Automatic API documentation** with Swagger UI
- **CORS support** for cross-origin requests
- **Health check endpoint**

## Project Structure

```
python-fastapi-101/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Option 1: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Run the main.py file
python main.py
```

### 4. Access the Application

- **API**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Basic Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check

### Item Management

- `GET /items` - Get all items
- `GET /items/{item_id}` - Get item by ID
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item
- `GET /items/search/` - Search items with filters

### Search Parameters

- `q` - Search by name (case-insensitive)
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter

## Example Usage

### Create an Item

```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Laptop",
       "description": "Gaming laptop",
       "price": 1299.99,
       "is_available": true
     }'
```

### Get All Items

```bash
curl -X GET "http://localhost:8000/items"
```

### Search Items

```bash
curl -X GET "http://localhost:8000/items/search/?q=laptop&min_price=1000"
```

## Data Model

### Item

```json
{
  "id": "uuid-string",
  "name": "string",
  "description": "string (optional)",
  "price": "number",
  "is_available": "boolean",
  "created_at": "datetime"
}
```

## Development

The application uses in-memory storage for simplicity. In a production environment, you would typically use a database like PostgreSQL, MySQL, or MongoDB.

### Hot Reload

The `--reload` flag enables automatic reloading when code changes are detected:

```bash
uvicorn main:app --reload
```

## Next Steps

- Add database integration (SQLAlchemy, MongoDB, etc.)
- Implement authentication and authorization
- Add input validation and error handling
- Create unit tests
- Add logging
- Implement rate limiting
- Add API versioning
