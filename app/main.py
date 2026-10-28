from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, products, suppliers, inventory, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory & Order Management API",
    description="Portfolio project for inventory, suppliers, purchase/sales orders, and stock movements.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(inventory.router)
app.include_router(orders.router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
