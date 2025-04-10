from pydantic import BaseModel, Field
from typing import List, Optional

class TagBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, 
                       regex="^[a-zA-Z0-9_\-]+$",
                       description="Nombre del tag (solo letras, números, guiones y underscores)")

class TagCreate(TagBase):
    pass

class TagInDB(TagBase):
    id: int
    
    class Config:
        orm_mode = True

class ProductTagRelation(BaseModel):
    producto_id: int
    tag_id: int

class ProductWithTags(BaseModel):
    id: int
    nombre: str
    tags: List[TagInDB]

class TagWithProducts(BaseModel):
    id: int
    nombre: str
    productos_count: int