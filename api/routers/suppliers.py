from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.dependecies import get_db
from schemas.product import ProductResponse
from services.supplier_service import SupplierService
from schemas.supplier import SupplierCreate, SupplierResponse, SupplierAddProduct

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/", status_code=201, response_model=SupplierResponse)
def create_supplier(supplier_create: SupplierCreate, session: Session = Depends(get_db)):
    supplier = SupplierService(session)

    try: 
        created_supplier = supplier.create_supplier(
            name=supplier_create.name, 
            email=supplier_create.email, 
            phone=supplier_create.phone)
        session.commit()
        session.refresh(created_supplier)

    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return created_supplier

@router.get("/", response_model=list[SupplierResponse])
def get_all_suppliers(session: Session = Depends(get_db)):

    return SupplierService(session).get_all_suppliers()

@router.get("/{id}", response_model=SupplierResponse)
def get_supplier(id: int, session: Session = Depends(get_db)):
    supplier_service = SupplierService(session)

    supplier = supplier_service.get_supplier(id)

    if supplier is None:
        raise HTTPException(
            status_code=404, 
            detail= "Supplier with given ID does not exists"
            )

    return supplier

@router.post("/{supplier_id}/products")
def add_product_to_supplier(
    supplier_id: int, 
    supplier_add_product: SupplierAddProduct, 
    session: Session = Depends(get_db)
    ):
    supplier_service = SupplierService(session)

    try: 
        supplier_service.add_product_to_supplier(supplier_id, sku=supplier_add_product.sku)
        session.commit()
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(e)) 

    return {
        "message": "Successfully",
        "supplier_id": supplier_id,
        "sku:": supplier_add_product.sku
    }

@router.get("/{supplier_id}/products", response_model=list[ProductResponse])
def get_supplier_products(supplier_id: int, session: Session = Depends(get_db)):
    supplier = SupplierService(session).get_supplier(supplier_id)
    if supplier is None: 
        raise HTTPException(status_code=404, detail="Supplier cannot be found")

    return supplier.products