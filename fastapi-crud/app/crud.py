from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy import or_, false
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


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: str = "desc",
) -> Dict[str, Any]:
    """
    Retrieve products with optional filtering, case-insensitive partial searching,
    sorting, and pagination.
    Execution order: 1. Filtering -> 2. Search -> 3. Sorting -> 4. Pagination.
    """
    query = db.query(models.Product)

    # 1. Filtering (AND logic between conditions)
    if category is not None:
        if hasattr(models.Product, "category"):
            query = query.filter(models.Product.category == category)
        else:
            # If model does not have category column, exact match returns empty result
            query = query.filter(false())

    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    # 2. Search (Case-insensitive partial match across existing text fields)
    if search is not None and search.strip():
        search_term = f"%{search.strip()}%"
        search_conditions = []
        for field_name in ["name", "title", "description"]:
            if hasattr(models.Product, field_name):
                col = getattr(models.Product, field_name)
                search_conditions.append(col.ilike(search_term))
        if search_conditions:
            query = query.filter(or_(*search_conditions))

    # 3. Sorting
    if sort_by is not None and sort_by.strip():
        sort_field = sort_by.strip()
        sort_col = None

        if sort_field == "price" and hasattr(models.Product, "price"):
            sort_col = models.Product.price
        elif sort_field == "created_at":
            if hasattr(models.Product, "created_at"):
                sort_col = models.Product.created_at
            else:
                # If created_at doesn't exist, check for another timestamp column
                for ts_col in ["updated_at", "timestamp", "date"]:
                    if hasattr(models.Product, ts_col):
                        sort_col = getattr(models.Product, ts_col)
                        break
                # If no timestamp column exists, fallback to sequential primary key 'id'
                if sort_col is None and hasattr(models.Product, "id"):
                    sort_col = models.Product.id
        elif hasattr(models.Product, sort_field) and sort_field in [
            "id",
            "name",
            "description",
            "in_stock",
            "user_id",
        ]:
            sort_col = getattr(models.Product, sort_field)

        if sort_col is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid sort_by field.",
            )

        if order.lower() == "asc":
            query = query.order_by(sort_col.asc())
        elif order.lower() == "desc":
            query = query.order_by(sort_col.desc())
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid order field. Supported values are 'asc' or 'desc'.",
            )
    else:
        # If sort_by is not provided, validate order parameter
        if order.lower() not in ("asc", "desc"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid order field. Supported values are 'asc' or 'desc'.",
            )

    # 4. Pagination (total must count records AFTER filtering/search but BEFORE pagination)
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items,
    }



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

