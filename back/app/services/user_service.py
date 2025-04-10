from sqlalchemy.orm import Session
from db.models import Usuario, Subasta

def get_user_by_id(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_user_auctions(db: Session, user_id: int):
    return db.query(Subasta).filter(Subasta.subastador_id == user_id).all()

def create_user(db: Session, user_data: dict):
    db_user = Usuario(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user