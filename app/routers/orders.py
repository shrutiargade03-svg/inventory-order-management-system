from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, OrderItem, Product, Supplier, StockMovement, User
from app.schemas import OrderCreate, OrderOut
from app.security import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=OrderOut, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.order_type == "purchase" and not payload.supplier_id:
        raise HTTPException(status_code=422, detail="Purchase orders require supplier_id")
    if payload.supplier_id and not db.get(Supplier, payload.supplier_id):
        raise HTTPException(status_code=404, detail="Supplier not found")
    order = Order(order_type=payload.order_type, supplier_id=payload.supplier_id,
                  notes=payload.notes, created_by=user.id, status="draft")
    db.add(order)
    try:
        db.flush()
        for item in payload.items:
            product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
            if not product or not product.is_active:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found or inactive")
            price = float(item.unit_price if item.unit_price is not None else product.unit_price)
            order.items.append(OrderItem(product_id=product.id, quantity=item.quantity, unit_price=price))
        db.commit()
        db.refresh(order)
        return order
    except Exception:
        db.rollback()
        raise

@router.get("", response_model=list[OrderOut])
def list_orders(order_type: str | None = None, skip: int = 0, limit: int = 50,
                db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Order)
    if order_type in ("sale", "purchase"):
        query = query.filter(Order.order_type == order_type)
    return query.order_by(Order.id.desc()).offset(max(skip, 0)).limit(min(max(limit, 1), 100)).all()

@router.post("/{order_id}/complete", response_model=OrderOut)
def complete_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).with_for_update().first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "draft":
        raise HTTPException(status_code=409, detail="Only draft orders can be completed")
    try:
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
            if order.order_type == "sale":
                if product.quantity < item.quantity:
                    raise HTTPException(status_code=409, detail=f"Insufficient stock for {product.name}")
                change, reason = -item.quantity, "sale"
            else:
                change, reason = item.quantity, "receipt"
            product.quantity += change
            db.add(StockMovement(product_id=product.id, quantity_change=change, reason=reason,
                                 note=f"Order #{order.id}", created_by=user.id))
        order.status = "completed"
        db.commit()
        db.refresh(order)
        return order
    except Exception:
        db.rollback()
        raise

@router.post("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "draft":
        raise HTTPException(status_code=409, detail="Only draft orders can be cancelled")
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order
