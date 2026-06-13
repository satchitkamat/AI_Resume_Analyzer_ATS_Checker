from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.core.database import Base

class CandidatePipeline(Base):

    __tablename__ = "candidate_pipline"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidate_id = Column(
        Integer,
        ForeignKey("resumes.id")
    )

    status = Column(
        String,
        default="Applied"
    )