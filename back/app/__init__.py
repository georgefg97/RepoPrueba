# Este archivo hace que Python trate el directorio como un paquete
# También puede contener inicializaciones importantes para la aplicación

from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Importaciones que se usarán en otros módulos
from .main import app
from db.session import SessionLocal

__all__ = ['app', 'SessionLocal']