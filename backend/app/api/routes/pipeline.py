from sqlalchemy.orm import Session

from app.models.candidate_pipeline import (
    CandidatePipeline
)

VALID_STATUSES = [

"Applied",

"Screening",

"Shortlisted",

"Interview Scheduled",

"Interviewed",

"Selected",

"Rejected",

"Hired"

]

def create_pipeline(
    db:Session,
    candidate_id: int
):
    pipeline = CandidatePipeline(
        candidate_id=candidate_id,
        status="Applied"
    )

    db.add(pipeline)

    db.commit()

    db.refresh(pipeline)

    return pipeline

def get_candidate_pipeline(
    db:Session,
    candidate_id:int
):
    return(
        db.query(
            CandidatePipeline
        )

        .filter(
            CandidatePipeline.candidate_id == candidate_id
        )

        .first()
    )

def update_pipeline_status(
    db:Session,
    candidate_id:int,
    status:str
):
    if status not in VALID_STATUSES:
        raise ValueError(
            "Invalid pipeline status"
        )
    
    candidate = get_candidate_pipeline(
        db,
        candidate_id
    )

    if not candidate:
        raise ValueError(
            "candidate pipeline not found"
        )
    
    candidate.status = status

    db.commit()

    db.refresh(candidate)

    return candidate

def auto_pipeline_status(
    ats_score:float,
    hiring_recommendation:dict
):
    decision = (
        hiring_recommendation.get("decision", "").lower()
    )

    if decision == "strong hire": 
        return "Shortlisted" 
    
    if decision == "hire": 
        return "Shortlisted" 
    
    if decision == "interview": 
        return "Interview Scheduled" 
    
    if decision == "reject": 
        return "Rejected" 
    
    if ats_score >= 80: 
        return "Shortlisted" 
    
    if ats_score >= 60: 
        return "Screening" 
    
    return "Rejected"

def get_pipeline_statistics(
    db:Session,
):
    stats = {}

    for status in VALID_STATUSES:
        stats[status] = (
            db.query(CandidatePipeline).filter(CandidatePipeline.status==status).count()
        )

    return stats