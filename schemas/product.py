from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal 

class ProductResponse(BaseModel): 
    id : int
    name : str
    sku : str
    price : Decimal
    quantity : int
    min_stock : int

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name : str = Field(min_length=1)
    sku : str = Field(min_length=1)
    price : Decimal = Field(gt=0)
    min_stock : int = Field(ge=0)

class ProductUpdate(BaseModel):
    name : str = Field(min_length=1)
    