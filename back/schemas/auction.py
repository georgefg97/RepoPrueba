from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class AuctionType(str, Enum):
    inglesa = "inglesa"
    holandesa = "holandesa"

class AuctionStatus(str, Enum):
    activa = "activa"
    pausada = "pausada"
    finalizada = "finalizada"
    cancelada = "cancelada"

class AuctionBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=500)
    tipo: AuctionType = AuctionType.inglesa
    precio_inicial: float = Field(..., gt=0)
    fecha_fin: datetime

class AuctionCreate(AuctionBase):
    subcategoria_id: int = Field(..., gt=0)

class AuctionUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=5, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=500)
    estado: Optional[AuctionStatus] = None

class AuctionInDB(AuctionBase):
    id: int
    subastador_id: int
    estado: AuctionStatus
    precio_actual: float
    fecha_inicio: datetime
    subcategoria_id: int

    class Config:
        orm_mode = True

class AuctionList(BaseModel):
    items: List[AuctionInDB]
    total: int