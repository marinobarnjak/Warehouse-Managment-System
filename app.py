from fastapi import FastAPI
from api.routers.products import router as product_router
from api.routers.inventory import router as inventory_router

app = FastAPI()
app.title="Warehouse Managment System"

@app.get('/')
def root():
    return {"message": "WMS API is running"}

app.include_router(product_router)
app.include_router(inventory_router)