from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import (
    get_db
)

from app.models.candidate_analysis import (
    CandidateAnalysis
)

from app.services.candidate_ranking import (
    rank_candidates
)

router = APIRouter(

    prefix="/candidate-ranking",

    tags=["Candidate Ranking"]
)


@router.get("/")
def get_candidate_ranking(

    db: Session = Depends(
        get_db
    )
):

    analyses = (
        db.query(
            CandidateAnalysis
        ).all()
    )

    candidates = []

    for analysis in analyses:

        candidates.append({

            "resume_id":
            analysis.resume_id,

            "ats_score":
            analysis.ats_score,

            "job_fit_score":
            analysis.job_fit_score,

            "credibility_score":
            analysis.credibility_score,

            "risk_score":
            analysis.risk_score,

            "interview_readiness_score":
            analysis.interview_readiness_score,

            "hiring_decision":
            analysis.hiring_decision
        })

    ranked_candidates = (
        rank_candidates(
            candidates
        )
    )

    return ranked_candidates