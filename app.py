from fastapi import FastAPI
from api.routers.products import router

app = FastAPI()
app.title="Warehouse Managment System"

@app.get('/')
def root():
    return {"message": "WMS API is running"}

app.include_router(router)