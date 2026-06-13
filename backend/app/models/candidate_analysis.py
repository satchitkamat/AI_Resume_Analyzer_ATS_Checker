from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class CandidateAnalysis(Base):

    __tablename__ = "candidate_analysis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    ats_score = Column(
        Float,
        default=0
    )

    credibility_score = Column(
        Float,
        default=0
    )

    job_fit_score = Column(
        Float,
        default=0
    )

    risk_score = Column(
        Float,
        default=0
    )

    interview_readiness_score = Column(
        Float,
        default=0
    )

    hiring_decision = Column(
        String,
        default="Pending"
    )

    pipeline_status = Column(
        String,
        default="Applied"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )