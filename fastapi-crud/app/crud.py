from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Retrieve a single product by its ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[models.Product]:
    """Retrieve a list of products with pagination support."""
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Create a new product record in the database."""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session, db_product: models.Product, product_update: schemas.ProductUpdate
) -> models.Product:
    """Update an existing product by dynamically applying changes from schema."""
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, db_product: models.Product) -> None:
    """Delete a product record from the database."""
    db.delete(db_product)
    db.commit()
