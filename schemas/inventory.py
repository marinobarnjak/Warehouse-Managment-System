from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime 

class StockMovementCreate(BaseModel):
    sku : str = Field(min_length=1)
    quantity : int = Field(gt=0)

class StockMovementResponse(BaseModel):
    id : int
    product_id : int
    movement_type : str
    quantity : int
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)
