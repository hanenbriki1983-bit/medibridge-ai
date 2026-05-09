from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import init_db
from app.services.chat_service import router as chat_router
from app.services.compliance_service import router as compliance_router
from app.services.dashboard_service import router as dashboard_router

app = FastAPI(title="MediBridge AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(chat_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(compliance_router, prefix="/api")
