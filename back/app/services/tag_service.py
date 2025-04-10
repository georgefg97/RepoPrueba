from sqlalchemy.orm import Session
from db.models import Tag, Producto, ProductoTags
from schemas.tag import TagInDB, ProductWithTags, TagWithProducts, TagCreate
from fastapi import HTTPException, status
from typing import List

def add_tag_to_product(db: Session, producto_id: int, tag_name: str) -> TagInDB:
    # Buscar producto
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    # Buscar o crear tag
    tag = db.query(Tag).filter(Tag.nombre == tag_name).first()
    if not tag:
        tag = Tag(nombre=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    
    # Verificar si la relación ya existe
    existing_relation = db.query(ProductoTags).filter(
        ProductoTags.producto_id == producto_id,
        ProductoTags.tag_id == tag.id
    ).first()
    
    if existing_relation:
        return TagInDB.from_orm(tag)
    
    # Crear la relación
    relation = ProductoTags(producto_id=producto_id, tag_id=tag.id)
    db.add(relation)
    db.commit()
    
    return TagInDB.from_orm(tag)

def get_product_tags(db: Session, producto_id: int) -> List[TagInDB]:
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    return [TagInDB.from_orm(tag) for tag in producto.tags]

def remove_tag_from_product(db: Session, producto_id: int, tag_id: int) -> None:
    relation = db.query(ProductoTags).filter(
        ProductoTags.producto_id == producto_id,
        ProductoTags.tag_id == tag_id
    ).first()
    
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación no encontrada"
        )
    
    db.delete(relation)
    db.commit()

def get_products_by_tag(db: Session, tag_name: str, limit: int = 100) -> List[ProductWithTags]:
    tag = db.query(Tag).filter(Tag.nombre == tag_name).first()
    if not tag:
        return []
    
    productos = db.query(Producto).join(ProductoTags).filter(
        ProductoTags.tag_id == tag.id
    ).limit(limit).all()
    
    return [ProductWithTags(
        id=producto.id,
        nombre=producto.nombre,
        tags=[TagInDB.from_orm(t) for t in producto.tags]
    ) for producto in productos]

def get_popular_tags(db: Session, limit: int = 10) -> List[TagWithProducts]:
    tags = db.query(
        Tag.id,
        Tag.nombre,
        db.func.count(ProductoTags.producto_id).label('productos_count')
    ).join(ProductoTags).group_by(Tag.id).order_by(
        db.func.count(ProductoTags.producto_id).desc()
    ).limit(limit).all()
    
    return [TagWithProducts(
        id=tag.id,
        nombre=tag.nombre,
        productos_count=tag.productos_count
    ) for tag in tags]

def delete_tag(db: Session, tag_id: int) -> None:
    """
    Elimina un tag completamente del sistema (incluyendo todas sus relaciones)
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag no encontrado"
        )
    
    # Eliminar todas las relaciones primero
    db.query(ProductoTags).filter(ProductoTags.tag_id == tag_id).delete()
    
    # Eliminar el tag
    db.delete(tag)
    db.commit()

def get_all_tags(db: Session, skip: int = 0, limit: int = 100) -> List[TagInDB]:
    """
    Obtiene todos los tags disponibles con paginación
    """
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return [TagInDB.from_orm(tag) for tag in tags]