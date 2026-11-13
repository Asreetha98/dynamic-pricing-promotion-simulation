from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.database.base import Base
from app.database.connection import engine
from app import models  # noqa: F401 - registers all ORM models
from app.routes import (auth_routes, product_routes, inventory_routes,
                        competitor_routes, promotion_routes, pricing_routes,
                        analytics_routes, cost_routes, order_routes, price_history_routes)

# Prototype convenience. Use Alembic migrations for deployment.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.1.0",
    description="Simulate explainable prices and promotions with margin and inventory guardrails.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": settings.app_name, "docs": "/docs", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

for router in [auth_routes.router, product_routes.router, inventory_routes.router,
               competitor_routes.router, promotion_routes.router, pricing_routes.router,
               analytics_routes.router, cost_routes.router, order_routes.router, price_history_routes.router]:
    app.include_router(router, prefix=settings.api_prefix)
