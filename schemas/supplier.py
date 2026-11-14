from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal 

class SupplierCreate(BaseModel):
    name : str = Field(min_length=1)
    email : str | None = None
    phone : str | None = None

class SupplierResponse(BaseModel):
    id : int
    name : str
    email : str | None
    phone : str | None
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class SupplierAddProduct(BaseModel):
    sku : str = Field(min_length=1)