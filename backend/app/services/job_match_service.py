def calculate_job_match(
    ats_score,
    github_skill_match,
    github_score,
    section_score
):
    job_match_score = (
        ats_score
    )

    job_match_score = ats_score

    job_match_feedback = get_job_match_feedback(
        job_match_score
    )
    return round(job_match_score,2)

def get_job_match_feedback(score):

    if score >= 85:
        return {
            "status": "Excellent Match",
            "chance": "High"
        }

    elif score >= 70:
        return {
            "status": "Good Match",
            "chance": "Medium-High"
        }

    elif score >= 50:
        return {
            "status": "Moderate Match",
            "chance": "Medium"
        }

    return {
        "status": "Low Match",
        "chance": "Low"
    }