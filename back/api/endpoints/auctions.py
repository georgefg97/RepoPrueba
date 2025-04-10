from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from db.session import get_db
from schemas.auction import (
    AuctionCreate,
    AuctionInDB,
    AuctionUpdate,
    AuctionList,
    AuctionStatus,
    AuctionType
)
from core.security import get_current_user
from db.models import Usuario
from services import auction_service

router = APIRouter()

@router.post("", response_model=AuctionInDB, status_code=status.HTTP_201_CREATED)
def create_auction(
    auction: AuctionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea una nueva subasta.
    Requiere autenticación.
    """
    return auction_service.create_auction(db, auction, current_user.id)

@router.get("", response_model=AuctionList)
def list_auctions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    estado: Optional[AuctionStatus] = None,
    tipo: Optional[AuctionType] = None,
    subcategoria_id: Optional[int] = Query(None, gt=0),
    db: Session = Depends(get_db)
):
    """
    Lista subastas con filtros opcionales.
    """
    auctions = auction_service.get_auctions(
        db,
        skip=skip,
        limit=limit,
        estado=estado.value if estado else None,
        tipo=tipo.value if tipo else None,
        subcategoria_id=subcategoria_id
    )
    total = db.query(Subasta).count()  # Simplificado, debería aplicar mismos filtros
    return AuctionList(items=auctions, total=total)

@router.get("/{auction_id}", response_model=AuctionInDB)
def get_auction(
    auction_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de una subasta específica.
    """
    auction = auction_service.get_auction_by_id(db, auction_id)
    if not auction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subasta no encontrada"
        )
    return auction