from typing import List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from . import models, schemas, crud, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Products CRUD API",
    description="A complete FastAPI REST API for managing Product resources with SQLite and SQLAlchemy.",
    version="1.0.0",
)


@app.post(
    "/auth/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)) -> models.User:
    """Register a new user by hashing their password."""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db=db, user=user)


@app.post(
    "/auth/login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
    summary="Login user and return JWT token",
)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Verify credentials and return a signed JWT access token."""
    user = crud.get_user_by_email(db, email=user_credentials.email)
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/users/me/items",
    response_model=List[schemas.ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Get items owned by current user",
)
def read_user_items(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> List[models.Product]:
    """Retrieve items owned by the currently logged-in user."""
    return crud.get_user_products(db=db, user_id=current_user.id, skip=skip, limit=limit)


@app.post(
    "/items",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
def create_item(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> models.Product:
    """Create a new product with name, price, description, and stock status, assigned to current user."""
    return crud.create_product(db=db, product=product, user_id=current_user.id)


@app.get(
    "/items",
    response_model=List[schemas.ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all products",
)
def read_items(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    db: Session = Depends(get_db),
) -> List[models.Product]:
    """Retrieve a list of products with optional pagination (skip and limit)."""
    return crud.get_products(db=db, skip=skip, limit=limit)


@app.get(
    "/items/{id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a product by ID",
)
def read_item(id: int, db: Session = Depends(get_db)) -> models.Product:
    """Retrieve a specific product by its ID."""
    db_product = crud.get_product(db=db, product_id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return db_product


@app.put(
    "/items/{id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a product",
)
def update_item(
    id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> models.Product:
    """Update an existing product by ID."""
    db_product = crud.get_product(db=db, product_id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    if db_product.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this item"
        )
    return crud.update_product(
        db=db, db_product=db_product, product_update=product_update
    )


@app.delete(
    "/items/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a product",
)
def delete_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
) -> Dict[str, Any]:
    """Delete a product by ID."""
    db_product = crud.get_product(db=db, product_id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    if db_product.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item"
        )
    crud.delete_product(db=db, db_product=db_product)
    return {
        "message": f"Product with ID {id} deleted successfully.",
        "deleted_id": id,
    }

