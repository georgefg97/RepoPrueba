import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
#from api.endpoints import auth

# Cargar variables de entorno
load_dotenv()

# Importar routers
from api.endpoints import (
    users,
    auctions,
    bids,
    tags
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación
    print("Iniciando aplicación...")
    yield
    # Código que se ejecuta al cerrar la aplicación
    print("Cerrando aplicación...")

app = FastAPI(
    title="Subasteltor API",
    description="API para el sistema de subastas Subasteltor",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url="/api/v1/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers con prefijo y tags
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
)
#app.include_router(auth.router, prefix="/api/v1")

app.include_router(
    auctions.router,
    prefix="/api/v1/auctions",
    tags=["auctions"]
)

app.include_router(
    bids.router,
    prefix="/api/v1/bids",
    tags=["bids"]
)

app.include_router(
    tags.router,
    prefix="/api/v1/tags",
    tags=["tags"]
)

# Health check endpoint
@app.get("/api/v1/health", tags=["system"])
def health_check():
    return {
        "status": "ok",
        "message": "Subasteltor API is running",
        "services": {
            "database": "healthy" if os.getenv("DATABASE_URL") else "unconfigured",
            "redis": "healthy" if os.getenv("REDIS_URL") else "unconfigured"
        }
    }

# Si se ejecuta directamente (para desarrollo)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )