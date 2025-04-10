from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BidBase(BaseModel):
    monto: float = Field(..., gt=0, description="Monto de la puja, debe ser mayor que 0")

class BidCreate(BidBase):
    subasta_id: int = Field(..., gt=0, description="ID de la subasta")

class BidInDB(BidBase):
    id: int
    usuario_id: int
    subasta_id: int
    fecha: datetime

    class Config:
        orm_mode = True