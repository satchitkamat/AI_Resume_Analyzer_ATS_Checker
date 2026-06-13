def calculate_candidate_rank(candidate):

    ats_score = candidate.get(
        "ats_score",
        0
    )

    job_fit_score = candidate.get(
        "job_fit_score",
        0
    )

    credibility_score = candidate.get(
        "credibility_score",
        0
    )

    interview_readiness_score = candidate.get(
        "interview_readiness_score",
        0
    )

    risk_score = candidate.get(
        "risk_score",
        0
    )

    overall_score = round(

        (
            ats_score * 0.30
            +
            job_fit_score * 0.25
            +
            credibility_score * 0.20
            +
            interview_readiness_score * 0.15
            +
            (100 - risk_score) * 0.10
        ),

        2
    )

    return overall_score


def rank_candidates(candidates):

    for candidate in candidates:

        candidate["overall_score"] = (
            calculate_candidate_rank(
                candidate
            )
        )

    candidates.sort(

        key=lambda x:
        x["overall_score"],

        reverse=True
    )

    for index, candidate in enumerate(
        candidates,
        start=1
    ):

        candidate["rank"] = index

    return candidates