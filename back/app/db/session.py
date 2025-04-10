from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración para XAMPP (MySQL)
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/subasteltor"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Esta es la función que se debe exportar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()