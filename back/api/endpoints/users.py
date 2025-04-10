from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.user import UserCreate, UserInDB, UserUpdate, UserLogin
from core.security import (
    get_password_hash, 
    create_access_token, 
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from db.models import Usuario
from datetime import timedelta



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function
def get_user(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

# Registro de usuario
@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        email=user.email,
        nombre=user.nombre,
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Login de usuario
@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user(db, email=user_data.email)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/token", tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Obtener usuario actual
@router.get("/me", response_model=UserInDB)
def read_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

# Actualizar usuario
@router.put("/me", response_model=UserInDB)
def update_current_user(
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user_id = payload.get("sub")
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_update.nombre is not None:
        db_user.nombre = user_update.nombre
    if user_update.plan is not None:
        db_user.plan = user_update.plan
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar usuario (solo para admins en producción)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # En producción, verificar que el usuario sea admin o el mismo usuario
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(db_user)
    db.commit()
    return None