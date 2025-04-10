from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.bid import BidCreate, BidInDB
from core.security import get_current_user
from db.models import Usuario
from services import bid_service

router = APIRouter()

@router.post("", response_model=BidInDB, status_code=status.HTTP_201_CREATED)
def create_bid(
    bid: BidCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea una nueva puja en una subasta.
    Validaciones:
    - Subasta debe existir y estar activa
    - Usuario no puede ser el subastador
    - Monto debe ser mayor que el precio actual
    - Subasta no debe haber finalizado
    """
    bid_data = bid.dict()
    bid_data['subasta_id'] = bid.subasta_id  # Asegurar el nombre correcto del campo
    
    return bid_service.create_bid(
        db=db,
        bid_data=bid_data,
        user_id=current_user.id
    )

@router.get("/{auction_id}", response_model=List[BidInDB])
def get_auction_bids(
    auction_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de pujas de una subasta específica,
    ordenadas por monto (de mayor a menor)
    """
    return bid_service.get_bids_by_auction(db, auction_id, limit)