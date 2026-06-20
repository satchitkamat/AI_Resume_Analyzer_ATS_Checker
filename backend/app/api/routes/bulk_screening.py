from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
)

from sqlalchemy.orm import Session

from typing import List

from app.core.database import (
    get_db
)

from app.services.bulk_screening import (
    bulk_screen_resumes
)

from app.api.routes.auth import (
    get_current_user
)

router = APIRouter(

    prefix="/bulk-screening",

    tags=["Bulk Screening"]
)


@router.post("/")
def bulk_screen(

    files: List[UploadFile] = File(...),

    job_description: str = Form(...),

    db: Session = Depends(
        get_db
    ),

    current_user = Depends(
        get_current_user
    )
):

    return bulk_screen_resumes(

        db=db,

        files=files,

        job_description=
        job_description,

        current_user=
        current_user
    )