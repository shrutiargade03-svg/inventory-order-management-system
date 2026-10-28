def register_and_login(client):
    response = client.post("/auth/register", json={
        "email": "admin@example.com", "full_name": "Test Admin", "password": "StrongPass123!"
    })
    assert response.status_code == 201
    response = client.post("/auth/login", data={
        "username": "admin@example.com", "password": "StrongPass123!"
    })
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}

def test_register_login_and_create_product(client):
    headers = register_and_login(client)
    response = client.post("/products", headers=headers, json={
        "sku": "KB-001", "name": "Keyboard", "unit_price": 899.0,
        "quantity": 10, "low_stock_threshold": 3
    })
    assert response.status_code == 201
    assert response.json()["quantity"] == 10
    assert client.get("/products", headers=headers).status_code == 200

def test_stock_movement_prevents_negative_inventory(client):
    headers = register_and_login(client)
    product = client.post("/products", headers=headers, json={
        "sku": "M-001", "name": "Mouse", "unit_price": 499, "quantity": 2
    }).json()
    response = client.post("/inventory/movements", headers=headers, json={
        "product_id": product["id"], "quantity_change": -5, "reason": "sale"
    })
    assert response.status_code == 409

def test_low_stock_endpoint(client):
    headers = register_and_login(client)
    client.post("/products", headers=headers, json={
        "sku": "LOW-001", "name": "Low Stock Item", "unit_price": 100,
        "quantity": 1, "low_stock_threshold": 5
    })
    response = client.get("/products/low-stock", headers=headers)
    assert response.status_code == 200
    assert any(p["sku"] == "LOW-001" for p in response.json())
