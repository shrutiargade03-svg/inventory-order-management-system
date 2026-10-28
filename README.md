# Inventory & Order Management System

A backend portfolio project built with **Python, FastAPI, PostgreSQL, SQLAlchemy, pytest, and Docker**. It demonstrates REST API design, relational data modeling, JWT authentication, role-based access control, inventory movements, order processing, and automated testing.

## Features

- Product CRUD, search, pagination, low-stock listing, and CSV export
- Supplier management
- Stock movement ledger with negative-stock protection
- Purchase and sales orders; completing an order updates stock and records movements in a database transaction
- JWT authentication and admin/staff roles
- Interactive OpenAPI documentation
- Docker Compose for API + PostgreSQL
- Pytest tests for health, authentication, products, and inventory validation

## Architecture

```text
Client / Swagger UI
        |
     FastAPI
        |
 Routers + Pydantic validation
        |
 SQLAlchemy ORM / transactions
        |
    PostgreSQL
```

## Run with Docker

Prerequisites: Docker Desktop (or Docker Engine) and Git.

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/inventory-order-management-system.git
   cd inventory-order-management-system
   ```
2. Create `.env` from the example and change the secret:
   ```bash
   cp .env.example .env
   ```
   On Windows PowerShell use:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Start the application:
   ```bash
   docker compose up --build
   ```
4. Open:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

The first account registered through `/auth/register` becomes the administrator. Subsequent registrations receive the staff role. For a real deployment, disable public self-registration and create users through a controlled admin workflow.

## Run locally without Docker

Prerequisites: Python 3.12+ and a running PostgreSQL database.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

Set `DATABASE_URL` and `SECRET_KEY` in your environment, then run:
```bash
uvicorn app.main:app --reload
```

## First API walkthrough

1. Open `/docs`.
2. Call `POST /auth/register` with:
   ```json
   {
     "email": "admin@example.com",
     "full_name": "Admin User",
     "password": "StrongPass123!"
   }
   ```
3. Call `POST /auth/login` using the email as `username` and the password. Copy the `access_token`.
4. Click **Authorize** in Swagger and enter the token.
5. Create a supplier using `POST /suppliers`.
6. Create a product using `POST /products`.
7. Create a purchase order with `POST /orders`, then complete it with `POST /orders/{order_id}/complete`.
8. Check `GET /inventory/movements`, `GET /products/low-stock`, and `GET /products/export.csv`.

Example product:
```json
{
  "sku": "KB-001",
  "name": "Mechanical Keyboard",
  "description": "USB keyboard",
  "unit_price": 2499.00,
  "quantity": 10,
  "low_stock_threshold": 3
}
```

Example purchase order:
```json
{
  "order_type": "purchase",
  "supplier_id": 1,
  "notes": "Initial stock purchase",
  "items": [
    {"product_id": 1, "quantity": 20, "unit_price": 2100}
  ]
}
```

Example sales order:
```json
{
  "order_type": "sale",
  "notes": "Customer order",
  "items": [
    {"product_id": 1, "quantity": 2}
  ]
}
```

Orders remain drafts until completed. Completing a purchase order adds stock; completing a sales order subtracts stock and rejects insufficient inventory.

## Run tests

```bash
pytest -q
```

Tests use an isolated in-memory SQLite database and do not require PostgreSQL. The application itself is configured for PostgreSQL by default.

## Main endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/auth/register` | Register account |
| POST | `/auth/login` | Get JWT token |
| GET | `/auth/me` | Current user |
| POST | `/products` | Create product (admin) |
| GET | `/products` | Search and paginate products |
| GET | `/products/low-stock` | Low-stock report |
| GET | `/products/export.csv` | CSV export |
| POST | `/suppliers` | Create supplier (admin) |
| POST | `/inventory/movements` | Record stock movement |
| GET | `/inventory/movements` | View stock ledger |
| POST | `/orders` | Create purchase/sales draft |
| POST | `/orders/{id}/complete` | Complete order and update stock |
| POST | `/orders/{id}/cancel` | Cancel a draft |

## Database tables

- `users`: identity, password hash, role, active flag
- `products`: SKU, price, quantity, reorder threshold
- `suppliers`: supplier contact details
- `orders`: order type, status, supplier and creator
- `order_items`: products and quantities per order
- `stock_movements`: immutable-style ledger entries for inventory changes

## Security notes

- Passwords are stored as hashes, not plain text.
- JWT secret is configurable through environment variables.
- Admin-only product/supplier creation and product updates are enforced.
- Never commit `.env`, credentials, production database URLs, or real customer data.
- This is a learning/portfolio implementation. Before production use, add database migrations (Alembic), rate limiting, stricter registration controls, structured logging, refresh-token strategy, and deployment-specific secret management.

## Roadmap

- [ ] Add Alembic migrations
- [ ] Add order detail response with nested line items and totals
- [ ] Add supplier update/delete endpoints
- [ ] Add role-permission matrix and audit log
- [ ] Add GitHub Actions CI for linting and tests
- [ ] Add deployment and monitoring
- [ ] Add frontend dashboard

## License

MIT — see `LICENSE`.
