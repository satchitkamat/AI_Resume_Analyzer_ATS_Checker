from fastapi import HTTPException

from app.models.candidate_pipeline import (
    CandidatePipeline
)


VALID_STATUSES = [

    "Applied",

    "Screening",

    "Shortlisted",

    "Interview Scheduled",

    "Interviewed",

    "Offer Sent",

    "Hired",

    "Rejected"
]


def create_pipeline_entry(
    db,
    resume_id
):

    pipeline = CandidatePipeline(

        resume_id=resume_id,

        status="Applied"
    )

    db.add(pipeline)

    db.commit()

    db.refresh(pipeline)

    return pipeline


def update_pipeline_status(

    db,

    resume_id,

    status
):

    if status not in VALID_STATUSES:

        raise HTTPException(

            status_code=400,

            detail="Invalid pipeline status"
        )

    pipeline = (

        db.query(
            CandidatePipeline
        )

        .filter(
            CandidatePipeline.resume_id ==
            resume_id
        )

        .first()
    )

    if not pipeline:

        raise HTTPException(

            status_code=404,

            detail="Pipeline record not found"
        )

    pipeline.status = status

    db.commit()

    db.refresh(pipeline)

    return pipeline


def get_pipeline_by_status(

    db,

    status
):

    return (

        db.query(
            CandidatePipeline
        )

        .filter(
            CandidatePipeline.status ==
            status
        )

        .all()
    )


def get_all_pipeline_candidates(
    db
):

    return (

        db.query(
            CandidatePipeline
        )

        .all()
    )