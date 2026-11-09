from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.dependecies import get_db
from services.product_service import ProductService
from schemas.product import ProductResponse, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def products(session: Session = Depends(get_db)):
    return ProductService(session).get_all_products()

@router.post("/", status_code = 201, response_model=ProductResponse)
def create_product(product: ProductCreate, session: Session = Depends(get_db)):
    product_service = ProductService(session)
    try:
        created_product = product_service.create_product(name=product.name, sku=product.sku, price=product.price, min_stock=product.min_stock)
        session.commit()
        session.refresh(created_product)

    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Product with this SKU already exists")

    return created_product

@router.get("/{sku}", response_model=ProductResponse)
def get_product(sku: str, session: Session = Depends(get_db)):
    product = ProductService(session)

    obtained_product = product.get_product(sku)
    
    if obtained_product == None: 
        raise HTTPException(status_code=404, detail="Product with given SKU does not exist")

    return obtained_product

@router.patch("/{sku}", response_model=ProductResponse)
def update_product(sku: str, product: ProductUpdate, session: Session = Depends(get_db)):
    update = ProductService(session)

    try:
        updated_product = update.update_product(sku, product.name)

        if updated_product is None: 
            raise HTTPException(status_code=404, detail="Product with given SKU does not exist")
        if updated_product == "":
            raise HTTPException(status_code=422, detail="Product SKU cannot be empty")

        session.commit()
        session.refresh(updated_product)

        return updated_product

    except ValueError as e: 
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{sku}", status_code=204)
def delete_product(sku: str, session: Session = Depends(get_db)):
    product = ProductService(session)
    try:
        existing_product = product.get_product(sku)
        if existing_product is None: 
            raise HTTPException(status_code=404, detail="Product with given SKU does not exist")
        product.delete_product(sku)
        session.commit()

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=409, detail="Product cannot be deleted")

    


    
    