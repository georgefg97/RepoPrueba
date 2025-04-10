from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from db.models import Subasta, Producto
from schemas.auction import AuctionInDB, AuctionCreate
from typing import List, Optional

def create_auction(db: Session, auction: AuctionCreate, user_id: int) -> AuctionInDB:
    db_auction = Subasta(
        subastador_id=user_id,
        titulo=auction.titulo,
        descripcion=auction.descripcion,
        tipo=auction.tipo.value,
        precio_inicial=auction.precio_inicial,
        precio_actual=auction.precio_inicial,
        fecha_inicio=datetime.utcnow(),
        fecha_fin=auction.fecha_fin,
        estado="activa",
        subcategoria_id=auction.subcategoria_id
    )
    
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    
    # Crear producto asociado (ejemplo básico)
    db_product = Producto(
        subasta_id=db_auction.id,
        nombre=auction.titulo,
        descripcion=auction.descripcion or ""
    )
    db.add(db_product)
    db.commit()
    
    return AuctionInDB.from_orm(db_auction)

def get_auctions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    subcategoria_id: Optional[int] = None
) -> List[AuctionInDB]:
    query = db.query(Subasta)
    
    if estado:
        query = query.filter(Subasta.estado == estado)
    if tipo:
        query = query.filter(Subasta.tipo == tipo)
    if subcategoria_id:
        query = query.filter(Subasta.subcategoria_id == subcategoria_id)
    
    auctions = query.offset(skip).limit(limit).all()
    return [AuctionInDB.from_orm(auction) for auction in auctions]

def get_auction_by_id(db: Session, auction_id: int) -> Optional[AuctionInDB]:
    auction = db.query(Subasta).filter(Subasta.id == auction_id).first()
    if auction:
        return AuctionInDB.from_orm(auction)
    return None