from pydantic import BaseModel
from typing import Optional

class CandidateSearchFilter(
    BaseModel
):
    min_ats_score: Optional[float] = None

    max_risk_score: Optional[float] = None

    min_job_fit_score: Optional[float] = None

    hiring_decision: Optional[str] = None

    min_interview_readiness: Optional[float] = None
    