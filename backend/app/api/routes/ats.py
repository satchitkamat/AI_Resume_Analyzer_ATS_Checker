from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.resume import Resume

from app.services.ats_service import (
    calculate_ats_score
)

router =APIRouter(
    prefix="/ats",
    tags=["ATS"]
)

@router.post("/analyze/{resume_id}")

def analyze_resume(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()
    if not Resume:

        return {
            "success" : False,
            "message" : "Resume not found"
        }
    
    result = calculate_ats_score(
        resume.extracted_text,
        job_description
    )

    return {
        "success": True,
        "resume_id": resume.id,
        "analysis": result
    }