from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.schemas.pipeline import (
    PipelineUpdateRequest
)

from app.services.pipeline import (

    update_pipeline_status,

    get_pipeline_by_status,

    get_all_pipeline_candidates
)

router = APIRouter(

    prefix="/pipeline",

    tags=["Pipeline"]
)


@router.patch("/{resume_id}")
def update_status(

    resume_id: int,

    request: PipelineUpdateRequest,

    db: Session = Depends(
        get_db
    )
):

    return update_pipeline_status(

        db,

        resume_id,

        request.status
    )


@router.get("/")
def get_all_candidates(

    db: Session = Depends(
        get_db
    )
):

    return get_all_pipeline_candidates(
        db
    )


@router.get("/status/{status}")
def get_candidates_by_status(

    status: str,

    db: Session = Depends(
        get_db
    )
):

    return get_pipeline_by_status(

        db,

        status
    )