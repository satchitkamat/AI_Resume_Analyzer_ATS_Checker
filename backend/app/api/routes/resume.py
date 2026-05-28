from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user import User

from app.services.auth_service import (
    get_current_user
)

from app.services.resume_service import (
    upload_resume
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@router.post("/upload")

def upload_resume_route(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return upload_resume(
        db=db,
        file=file,
        current_user=current_user
    )