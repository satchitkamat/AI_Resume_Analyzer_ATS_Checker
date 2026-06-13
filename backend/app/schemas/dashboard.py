from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_candidates: int

    shortlisted_candidates: int

    rejected_candidates: int

    hired_candidates: int

    interview_ready_candidates: int

    high_risk_candidates: int

    average_ats_score: float

    average_risk_score: float