from sqlalchemy.orm import Session
from datetime import datetime
from db.models import Puja, Subasta
from schemas.bid import BidInDB
from fastapi import HTTPException, status

def create_bid(
    db: Session,
    bid_data: dict,
    user_id: int
) -> BidInDB:
    # 1. Verificar que la subasta existe y está activa
    subasta = db.query(Subasta).filter(
        Subasta.id == bid_data['subasta_id'],
        Subasta.estado == 'activa'
    ).first()

    if not subasta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La subasta no existe o no está activa"
        )

    # 2. Verificar que el usuario no es el subastador
    if subasta.subastador_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes pujar en tu propia subasta"
        )

    # 3. Verificar que el monto es mayor que el precio actual
    if bid_data['monto'] <= subasta.precio_actual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El monto debe ser mayor que {subasta.precio_actual}"
        )

    # 4. Verificar que la subasta no ha finalizado
    if subasta.fecha_fin < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La subasta ya ha finalizado"
        )

    # 5. Crear la puja
    db_bid = Puja(
        subasta_id=bid_data['subasta_id'],
        usuario_id=user_id,
        monto=bid_data['monto']
    )
    db.add(db_bid)

    # 6. Actualizar el precio actual de la subasta
    subasta.precio_actual = bid_data['monto']
    db.add(subasta)

    db.commit()
    db.refresh(db_bid)

    return BidInDB.from_orm(db_bid)

def get_bids_by_auction(
    db: Session,
    auction_id: int,
    limit: int = 100
) -> list[BidInDB]:
    bids = db.query(Puja).filter(
        Puja.subasta_id == auction_id
    ).order_by(
        Puja.monto.desc()
    ).limit(limit).all()
    
    return [BidInDB.from_orm(bid) for bid in bids]