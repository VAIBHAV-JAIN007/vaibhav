from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routers import account, auth, market

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="0.1.0", description="Trading research API. No broker order execution.")
origins = [item.strip() for item in settings.cors_origins.split(",") if item.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET","POST","OPTIONS"], allow_headers=["Authorization","Content-Type"])
app.include_router(auth.router, prefix="/api/v1")
app.include_router(market.router, prefix="/api/v1")
app.include_router(account.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status":"ok","service":"gati-api"}

@app.get("/")
def root():
    return {"name":settings.app_name,"docs":"/docs","health":"/health"}
