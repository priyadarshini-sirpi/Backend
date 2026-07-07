from typing import List, Optional
from sqlalchemy.orm import Session
from . import auth, models, schemas


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Retrieve a single user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user record in the database with a hashed password."""
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Retrieve a single product by its ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[models.Product]:
    """Retrieve a list of products with pagination support."""
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_user_products(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[models.Product]:
    """Retrieve a list of products owned by a specific user."""
    return db.query(models.Product).filter(models.Product.user_id == user_id).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate, user_id: int) -> models.Product:
    """Create a new product record in the database assigned to a specific user."""
    db_product = models.Product(**product.model_dump(), user_id=user_id)
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

