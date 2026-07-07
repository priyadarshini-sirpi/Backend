from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    email: str = Field(..., min_length=3, description="User email address")
    password: str = Field(..., min_length=6, description="User password")


class UserLogin(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the product")
    description: Optional[str] = Field(None, description="Description of the product")
    price: float = Field(..., gt=0, description="Price of the product")
    in_stock: bool = Field(True, description="Whether the product is in stock")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Name of the product")
    description: Optional[str] = Field(None, description="Description of the product")
    price: Optional[float] = Field(None, gt=0, description="Price of the product")
    in_stock: Optional[bool] = Field(None, description="Whether the product is in stock")


class ProductResponse(ProductBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

