def generate_ai_feedback(
    ats_score,
    matched_skills,
    missing_skills,
    suggestions
):
    feedback = []

    if ats_score >= 80:
        feedback.append(
            "Your resume is strongly aligned with the job description."
        )

    elif ats_score >=60:
        feedback.append(
            "Your resume has moderate alignment with the job description."
        )

    else:
        feedback.append(
            "Your resume requires significant improvements."
        )

    if missing_skills:
        feedback.append(
            f"Consider adding: {', '.join(missing_skills[:5])}"
        )

    feedback.extend(suggestions)

    return feedback