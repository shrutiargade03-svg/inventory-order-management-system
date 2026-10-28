from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProductCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=60)
    name: str = Field(min_length=1, max_length=160)
    description: str | None = None
    unit_price: float = Field(ge=0)
    quantity: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=5, ge=0)

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    unit_price: float | None = Field(default=None, ge=0)
    low_stock_threshold: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sku: str
    name: str
    description: str | None
    unit_price: float
    quantity: int
    low_stock_threshold: int
    is_active: bool

class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None

class SupplierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str | None
    phone: str | None
    address: str | None

class StockMovementCreate(BaseModel):
    product_id: int
    quantity_change: int
    reason: str = Field(pattern="^(receipt|sale|adjustment|return)$")
    note: str | None = None

class StockMovementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    quantity_change: int
    reason: str
    note: str | None
    created_at: datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float | None = Field(default=None, ge=0)

class OrderCreate(BaseModel):
    order_type: str = Field(pattern="^(sale|purchase)$")
    supplier_id: int | None = None
    notes: str | None = None
    items: list[OrderItemCreate] = Field(min_length=1)

class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_type: str
    status: str
    supplier_id: int | None
    notes: str | None
    created_at: datetime
