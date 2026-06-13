from app.models.candidate_analysis import (
    CandidateAnalysis
)


def search_candidates(
    query,
    filters
):

    if filters.min_ats_score:

        query = query.filter(

            CandidateAnalysis.ats_score >=
            filters.min_ats_score
        )

    if filters.max_risk_score:

        query = query.filter(

            CandidateAnalysis.risk_score <=
            filters.max_risk_score
        )

    if filters.min_job_fit_score:

        query = query.filter(

            CandidateAnalysis.job_fit_score >=
            filters.min_job_fit_score
        )

    if filters.hiring_decision:

        query = query.filter(

            CandidateAnalysis.hiring_decision ==
            filters.hiring_decision
        )

    if filters.min_interview_readiness:

        query = query.filter(

            CandidateAnalysis.interview_readiness_score >=
            filters.min_interview_readiness
        )

    return query.all()