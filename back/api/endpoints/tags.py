from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.tag import (
    TagInDB,
    ProductWithTags,
    TagWithProducts,
    TagCreate
)
from core.security import get_current_user
from services import tag_service

router = APIRouter(tags=["tags"])

@router.post("/productos/{producto_id}/tags", response_model=TagInDB)
def add_tag_to_product(
    producto_id: int,
    tag: TagCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Añade un tag a un producto.
    Si el tag no existe, se crea automáticamente.
    Requiere autenticación.
    """
    return tag_service.add_tag_to_product(db, producto_id, tag.nombre)

@router.get("/productos/{producto_id}/tags", response_model=List[TagInDB])
def get_product_tags(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los tags asociados a un producto específico.
    """
    return tag_service.get_product_tags(db, producto_id)

@router.delete("/productos/{producto_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tag_from_product(
    producto_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Elimina un tag de un producto.
    Requiere autenticación.
    """
    tag_service.remove_tag_from_product(db, producto_id, tag_id)
    return None

@router.get("/tags/{tag_name}/productos", response_model=List[ProductWithTags])
def get_products_by_tag(
    tag_name: str,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Busca productos por tag.
    """
    return tag_service.get_products_by_tag(db, tag_name, limit)

@router.get("/tags/populares", response_model=List[TagWithProducts])
def get_popular_tags(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Obtiene los tags más populares (con más productos asociados).
    """
    return tag_service.get_popular_tags(db, limit)

@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Elimina completamente un tag del sistema (incluyendo todas sus relaciones).
    Requiere autenticación.
    """
    tag_service.delete_tag(db, tag_id)
    return None

@router.get("/tags/", response_model=List[TagInDB])
def get_all_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los tags disponibles con paginación.
    """
    return tag_service.get_all_tags(db, skip=skip, limit=limit)