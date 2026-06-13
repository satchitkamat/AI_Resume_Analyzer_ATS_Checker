from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.candidate_analysis import CandidateAnalysis
from app.schemas.candidate_search import CandidateSearchFilter
from app.services.candidate_search import search_candidates

router = APIRouter(
    prefix="/candidate-search",
    tags=["candidate-search"]
)

@router.post("/")
def candidate_search(
    filters: CandidateSearchFilter,
    db: Session = Depends(get_db)
):
    query = db.query(CandidateAnalysis)

    results = search_candidates(query, filters)

    return results