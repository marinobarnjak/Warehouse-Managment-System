from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from requests import Response 

from api.dependecies import get_db
from services.inventory_services import InventoryService
from services.product_service import ProductService
from schemas.inventory import StockMovementCreate, StockMovementResponse
from schemas.product import ProductResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/receive", status_code=201)
def receive_stock(stock_movement: StockMovementCreate, session: Session = Depends(get_db)):
    product_service = ProductService(session)
    inventory_service = InventoryService(session, product_service)

    try:        
        inventory_service.receive_stock(stock_movement.sku, stock_movement.quantity)
        session.commit()

    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {
    "message": "Stock received successfully",
    "sku": stock_movement.sku,
    "quantity": stock_movement.quantity
}

@router.post("/issue", status_code=201)
def issue_stock(stock_movement: StockMovementCreate, session: Session = Depends(get_db)):
    product_service = ProductService(session)
    inventory_service = InventoryService(session, product_service)

    try:        
        if not product_service.get_product(stock_movement.sku):
            raise HTTPException(status_code=404, detail="Product does not exist")
        inventory_service.issue_stock(stock_movement.sku, stock_movement.quantity)
        session.commit()
    
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    
    return {
        "message": "Stock issued successfully",
        "sku": stock_movement.sku,
        "quantity": inventory_service.get_stock(stock_movement.sku)
    }

@router.get("/stock/{sku}")
def get_stock(sku: str, session: Session = Depends(get_db)):
    product_service = ProductService(session)
    inventory_service = InventoryService(session, product_service)

    try:
        inventory_service.get_stock(sku)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "message": f"Stock with the given SKU: {sku}",
        "sku": sku,
        "quantity": inventory_service.get_stock(sku)
    }

@router.get("/low-stock", response_model=list[ProductResponse])
def get_low_stock_products(session: Session = Depends(get_db)):
    product_service = ProductService(session)
    inventory_service = InventoryService(session, product_service)

    return inventory_service.get_low_stock_products()

@router.get("/movements", response_model=list[StockMovementResponse])
def get_all_movements(session: Session = Depends(get_db)):
    product_service = ProductService(session)
    inventory_service = InventoryService(session, product_service)

    return inventory_service.get_all_movements()