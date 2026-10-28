from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, StockMovement, User
from app.schemas import StockMovementCreate, StockMovementOut
from app.security import get_current_user

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/movements", response_model=StockMovementOut, status_code=201)
def create_movement(payload: StockMovementCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == payload.product_id).with_for_update().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if payload.quantity_change == 0:
        raise HTTPException(status_code=422, detail="Quantity change cannot be zero")
    if product.quantity + payload.quantity_change < 0:
        raise HTTPException(status_code=409, detail="Insufficient stock")
    product.quantity += payload.quantity_change
    movement = StockMovement(**payload.model_dump(), created_by=user.id)
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement

@router.get("/movements", response_model=list[StockMovementOut])
def list_movements(product_id: int | None = None, skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(StockMovement)
    if product_id is not None:
        query = query.filter(StockMovement.product_id == product_id)
    return query.order_by(StockMovement.id.desc()).offset(max(skip, 0)).limit(min(max(limit, 1), 100)).all()
