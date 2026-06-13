from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.core.database import get_db

from fastapi import Depends

from app.services.dashboard import (
    get_dashboard_metrics
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    db: Session = Depends(
        get_db
    )
):

    return get_dashboard_metrics(
        db
    )