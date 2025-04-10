from pydantic_settings import BaseSettings
from pydantic import Field, MySQLDsn, RedisDsn, SecretStr, AmqpDsn, PostgresDsn
from typing import Literal, Optional

class Settings(BaseSettings):
    # 1. Configuración básica de la aplicación
    APP_ENV: Literal['development', 'staging', 'production'] = Field(
        default='development',
        description="Entorno de ejecución",
        json_schema_extra={"examples": ["development", "production"]}
    )
    
    APP_HOST: str = Field(
        default="0.0.0.0",
        description="Host de la aplicación",
        pattern=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    )
    
    APP_PORT: int = Field(
        default=8000,
        description="Puerto de la aplicación",
        gt=1024,
        lt=65535
    )
    
    APP_VERSION: str = Field(
        default="1.0.0",
        description="Versión de la API"
    )

    # 2. Configuración de base de datos
    DATABASE_URL: MySQLDsn = Field(
        default="mysql+mysqlconnector://user:password@db:3306/subasteltor",
        description="URL de conexión a MySQL",
        examples=["mysql+mysqlconnector://user:password@db:3306/dbname"]
    )
    
    DB_POOL_SIZE: int = Field(
        default=5,
        description="Tamaño máximo del pool de conexiones",
        gt=0,
        le=20
    )
    
    DB_POOL_RECYCLE: int = Field(
        default=3600,
        description="Tiempo en segundos para reciclar conexiones"
    )

    # 3. Configuración de Redis
    REDIS_URL: RedisDsn = Field(
        default="redis://redis:6379/0",
        description="URL de conexión a Redis para caché"
    )
    
    REDIS_CACHE_TTL: int = Field(
        default=300,
        description="TTL en segundos para caché Redis",
        gt=0
    )

    # 4. Configuración de seguridad
    JWT_SECRET: SecretStr = Field(
        default=SecretStr("change_this_to_strong_secret_32_chars_min"),
        description="Clave secreta para JWT",
        min_length=32
    )
    
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="Algoritmo para JWT"
    )
    
    JWT_EXPIRE_MINUTES: int = Field(
        default=1440,
        description="Tiempo de expiración del token en minutos"
    )

    # 5. Configuración CORS
    CORS_ORIGINS: list[str] = Field(
        default=["*"],
        description="Lista de orígenes permitidos para CORS"
    )
    
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        description="Permitir credenciales en CORS"
    )

    # 6. Configuración de WebSockets (para pujas en tiempo real)
    WS_MAX_CONNECTIONS: int = Field(
        default=100,
        description="Máximo de conexiones WebSocket simultáneas"
    )

    # 7. Configuración de subastas
    AUCTION_CLOSE_BUFFER: int = Field(
        default=300,
        description="Tiempo en segundos para extender subasta si hay pujas recientes"
    )
    
    BID_INCREMENT_PERCENT: float = Field(
        default=5.0,
        description="Incremento mínimo porcentual para nuevas pujas",
        gt=0
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "SUBASTELTOR_"
        extra = "ignore"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"
    
    @property
    def sqlalchemy_config(self) -> dict:
        return {
            "url": self.DATABASE_URL.unicode_string(),
            "pool_size": self.DB_POOL_SIZE,
            "pool_recycle": self.DB_POOL_RECYCLE,
            "echo": False if self.is_production else True
        }

settings = Settings()