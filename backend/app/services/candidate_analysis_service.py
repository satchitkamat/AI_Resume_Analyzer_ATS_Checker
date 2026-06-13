from sqlalchemy.orm import Session

from app.models.candidate_analysis import (
    CandidateAnalysis
)

def save_candidate_analysis(

    db: Session,

    resume_id,

    ats_score,

    candidate_validation,

    risk_analysis,

    interview_readiness,

    hiring_recommendation,

    pipeline_status="Applied"

):
    analysis = CandidateAnalysis(

        resume_id=resume_id,
    
        ats_score=float(ats_score),
    
        credibility_score=float(
            candidate_validation.get(
                "credibility_score",
                0
            )
        ),
    
        job_fit_score=float(
            candidate_validation.get(
                "job_fit_score",
                0
            )
        ),
    
        risk_score=float(
            risk_analysis.get(
                "risk_score",
                0
            )
        ),
    
        interview_readiness_score=float(
            interview_readiness.get(
                "interview_readiness_score",
                0
            )
        ),
    
        hiring_decision=
        str(
            hiring_recommendation.get(
                "recommendation",
                "Pending"
            )
        ),
    
        pipeline_status=
        str(pipeline_status)
    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    return analysis