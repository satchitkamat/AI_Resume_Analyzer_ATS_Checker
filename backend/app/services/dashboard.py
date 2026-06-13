from sqlalchemy.orm import Session

from app.models.resume import Resume

from app.models.candidate_analysis import (
    CandidateAnalysis
)

from app.models.candidate_pipeline import (
    CandidatePipeline
)


def get_dashboard_metrics(
    db: Session
):

    total_candidates = (
        db.query(
            Resume
        ).count()
    )

    shortlisted_candidates = (
        db.query(
            CandidatePipeline
        )
        .filter(
            CandidatePipeline.status ==
            "Shortlisted"
        )
        .count()
    )

    rejected_candidates = (
        db.query(
            CandidatePipeline
        )
        .filter(
            CandidatePipeline.status ==
            "Rejected"
        )
        .count()
    )

    hired_candidates = (
        db.query(
            CandidatePipeline
        )
        .filter(
            CandidatePipeline.status ==
            "Hired"
        )
        .count()
    )

    interview_ready_candidates = (
        db.query(
            CandidateAnalysis
        )
        .filter(
            CandidateAnalysis
            .interview_readiness_score >= 70
        )
        .count()
    )

    high_risk_candidates = (
        db.query(
            CandidateAnalysis
        )
        .filter(
            CandidateAnalysis.risk_score >= 70
        )
        .count()
    )

    analyses = (
        db.query(
            CandidateAnalysis
        ).all()
    )

    if analyses:

        average_ats_score = round(

            sum(
                analysis.ats_score
                for analysis in analyses
            )
            /
            len(analyses),

            2
        )

        average_risk_score = round(

            sum(
                analysis.risk_score
                for analysis in analyses
            )
            /
            len(analyses),

            2
        )

        average_job_fit_score = round(

            sum(
                analysis.job_fit_score
                for analysis in analyses
            )
            /
            len(analyses),

            2
        )

        average_credibility_score = round(

            sum(
                analysis.credibility_score
                for analysis in analyses
            )
            /
            len(analyses),

            2
        )

    else:

        average_ats_score = 0

        average_risk_score = 0

        average_job_fit_score = 0

        average_credibility_score = 0

    return {

        "total_candidates":
        total_candidates,

        "shortlisted_candidates":
        shortlisted_candidates,

        "rejected_candidates":
        rejected_candidates,

        "hired_candidates":
        hired_candidates,

        "interview_ready_candidates":
        interview_ready_candidates,

        "high_risk_candidates":
        high_risk_candidates,

        "average_ats_score":
        average_ats_score,

        "average_risk_score":
        average_risk_score,

        "average_job_fit_score":
        average_job_fit_score,

        "average_credibility_score":
        average_credibility_score
    }