from pydantic import BaseModel


class CandidateRankingResponse(
    BaseModel
):

    rank: int

    resume_id: int

    overall_score: float

    ats_score: float

    job_fit_score: float

    credibility_score: float

    risk_score: float

    interview_readiness_score: float

    hiring_decision: str