from fastapi import APIRouter

from app.database.db import get_dashboard_summary
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary() -> DashboardSummary:
    data = get_dashboard_summary()
    return DashboardSummary(**data)
