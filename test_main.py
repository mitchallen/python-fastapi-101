import pytest
from fastapi.testclient import TestClient
from main import app, items_db
from datetime import datetime

# Create a test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test"""
    items_db.clear()
    yield
    items_db.clear()


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_endpoint(self):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to FastAPI Demo!"
        assert data["version"] == "1.0.0"


class TestHealthCheck:
    """Tests for the health check endpoint"""
    
    def test_health_check(self):
        """Test that health check returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestItemCRUD:
    """Tests for CRUD operations on items"""
    
    def test_create_item(self):
        """Test creating a new item"""
        item_data = {
            "name": "Test Item",
            "description": "A test item",
            "price": 29.99,
            "is_available": True
        }
        response = client.post("/items", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == item_data["name"]
        assert data["description"] == item_data["description"]
        assert data["price"] == item_data["price"]
        assert data["is_available"] == item_data["is_available"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_item_minimal(self):
        """Test creating an item with minimal required fields"""
        item_data = {
            "name": "Minimal Item",
            "price": 10.0
        }
        response = client.post("/items", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == item_data["name"]
        assert data["price"] == item_data["price"]
        assert data["is_available"] == True  # Default value
        assert data["description"] is None
    
    def test_get_all_items_empty(self):
        """Test getting all items when database is empty"""
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_items(self):
        """Test getting all items"""
        # Create some items
        item1 = {"name": "Item 1", "price": 10.0}
        item2 = {"name": "Item 2", "price": 20.0}
        client.post("/items", json=item1)
        client.post("/items", json=item2)
        
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] in ["Item 1", "Item 2"]
        assert data[1]["name"] in ["Item 1", "Item 2"]
    
    def test_get_item_by_id(self):
        """Test getting an item by ID"""
        # Create an item
        item_data = {"name": "Test Item", "price": 15.99}
        create_response = client.post("/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Get the item by ID
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == item_data["name"]
        assert data["price"] == item_data["price"]
    
    def test_get_item_not_found(self):
        """Test getting a non-existent item returns 404"""
        response = client.get("/items/non-existent-id")
        assert response.status_code == 404
        assert "Item not found" in response.json()["detail"]
    
    def test_update_item(self):
        """Test updating an item"""
        # Create an item
        item_data = {"name": "Original Name", "price": 10.0}
        create_response = client.post("/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Update the item
        update_data = {"name": "Updated Name", "price": 20.0}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["price"] == 20.0
    
    def test_update_item_partial(self):
        """Test partial update of an item"""
        # Create an item
        item_data = {"name": "Original Name", "price": 10.0, "description": "Original description"}
        create_response = client.post("/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Update only the name
        update_data = {"name": "Updated Name"}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["price"] == 10.0  # Should remain unchanged
        assert data["description"] == "Original description"  # Should remain unchanged
    
    def test_update_item_not_found(self):
        """Test updating a non-existent item returns 404"""
        update_data = {"name": "Updated Name"}
        response = client.put("/items/non-existent-id", json=update_data)
        assert response.status_code == 404
        assert "Item not found" in response.json()["detail"]
    
    def test_delete_item(self):
        """Test deleting an item"""
        # Create an item
        item_data = {"name": "Item to Delete", "price": 15.0}
        create_response = client.post("/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Delete the item
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert "Item deleted successfully" in data["message"]
        assert data["deleted_item"]["id"] == item_id
        
        # Verify item is deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_delete_item_not_found(self):
        """Test deleting a non-existent item returns 404"""
        response = client.delete("/items/non-existent-id")
        assert response.status_code == 404
        assert "Item not found" in response.json()["detail"]


class TestSearch:
    """Tests for the search functionality"""
    
    def test_search_all_items(self):
        """Test search without filters returns all items"""
        # Create some items
        client.post("/items", json={"name": "Laptop", "price": 1000.0})
        client.post("/items", json={"name": "Mouse", "price": 25.0})
        
        response = client.get("/items/search/")
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    def test_search_by_name(self):
        """Test searching items by name"""
        # Create items
        client.post("/items", json={"name": "Laptop", "price": 1000.0})
        client.post("/items", json={"name": "Mouse", "price": 25.0})
        client.post("/items", json={"name": "Laptop Stand", "price": 50.0})
        
        response = client.get("/items/search/?q=laptop")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("laptop" in item["name"].lower() for item in data)
    
    def test_search_by_name_case_insensitive(self):
        """Test that search is case-insensitive"""
        client.post("/items", json={"name": "LAPTOP", "price": 1000.0})
        client.post("/items", json={"name": "Mouse", "price": 25.0})
        
        response = client.get("/items/search/?q=laptop")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "LAPTOP"
    
    def test_search_by_min_price(self):
        """Test searching items by minimum price"""
        client.post("/items", json={"name": "Item 1", "price": 50.0})
        client.post("/items", json={"name": "Item 2", "price": 100.0})
        client.post("/items", json={"name": "Item 3", "price": 150.0})
        
        response = client.get("/items/search/?min_price=100")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(item["price"] >= 100.0 for item in data)
    
    def test_search_by_max_price(self):
        """Test searching items by maximum price"""
        client.post("/items", json={"name": "Item 1", "price": 50.0})
        client.post("/items", json={"name": "Item 2", "price": 100.0})
        client.post("/items", json={"name": "Item 3", "price": 150.0})
        
        response = client.get("/items/search/?max_price=100")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(item["price"] <= 100.0 for item in data)
    
    def test_search_by_price_range(self):
        """Test searching items by price range"""
        client.post("/items", json={"name": "Item 1", "price": 50.0})
        client.post("/items", json={"name": "Item 2", "price": 100.0})
        client.post("/items", json={"name": "Item 3", "price": 150.0})
        client.post("/items", json={"name": "Item 4", "price": 200.0})
        
        response = client.get("/items/search/?min_price=75&max_price=175")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(75.0 <= item["price"] <= 175.0 for item in data)
    
    def test_search_combined_filters(self):
        """Test searching with name and price filters"""
        client.post("/items", json={"name": "Laptop", "price": 1000.0})
        client.post("/items", json={"name": "Laptop Stand", "price": 50.0})
        client.post("/items", json={"name": "Mouse", "price": 25.0})
        
        response = client.get("/items/search/?q=laptop&min_price=75")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Laptop"
        assert data[0]["price"] == 1000.0
    
    def test_search_no_results(self):
        """Test search that returns no results"""
        client.post("/items", json={"name": "Laptop", "price": 1000.0})
        
        response = client.get("/items/search/?q=tablet")
        assert response.status_code == 200
        assert response.json() == []


class TestValidation:
    """Tests for input validation"""
    
    def test_create_item_missing_required_fields(self):
        """Test creating item without required fields"""
        response = client.post("/items", json={})
        assert response.status_code == 422  # Validation error
    
    def test_create_item_missing_name(self):
        """Test creating item without name"""
        response = client.post("/items", json={"price": 10.0})
        assert response.status_code == 422
    
    def test_create_item_missing_price(self):
        """Test creating item without price"""
        response = client.post("/items", json={"name": "Test Item"})
        assert response.status_code == 422
    
    def test_create_item_invalid_price_type(self):
        """Test creating item with invalid price type"""
        response = client.post("/items", json={"name": "Test", "price": "not a number"})
        assert response.status_code == 422
    
    def test_create_item_negative_price(self):
        """Test creating item with negative price (should work, but testing validation)"""
        response = client.post("/items", json={"name": "Test", "price": -10.0})
        # Pydantic allows negative prices by default, so this should succeed
        # If business logic required, we'd add custom validation
        assert response.status_code == 200
