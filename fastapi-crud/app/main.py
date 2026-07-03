from typing import List, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Products CRUD API",
    description="A complete FastAPI REST API for managing Product resources with SQLite and SQLAlchemy.",
    version="1.0.0",
)


@app.post(
    "/items",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
def create_item(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
) -> models.Product:
    """Create a new product with name, price, description, and stock status."""
    return crud.create_product(db=db, product=product)


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
) -> models.Product:
    """Update an existing product by ID."""
    db_product = crud.get_product(db=db, product_id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return crud.update_product(
        db=db, db_product=db_product, product_update=product_update
    )


@app.delete(
    "/items/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a product",
)
def delete_item(id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Delete a product by ID."""
    db_product = crud.get_product(db=db, product_id=id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    crud.delete_product(db=db, db_product=db_product)
    return {
        "message": f"Product with ID {id} deleted successfully.",
        "deleted_id": id,
    }
