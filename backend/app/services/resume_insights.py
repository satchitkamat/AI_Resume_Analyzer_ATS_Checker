def get_resume_insights(
        quality,
        matched_skills,
        missing_skills,
        section_scores
):
    strengths = []
    weaknesses = []

    # Contact checks
    if quality["has_email"]:
        strengths.append(
            "Professional email found"
        )
    else:
        weaknesses.append(
            "Email address missing"
        )

    if quality["has_phone"]:
        strengths.append(
            "Phone number found"
        )
    else:
        weaknesses.append(
            "Phone number missing"
        )
    
    if quality["has_linkedin"]:
        strengths.append(
            "LinkedIn profile included"
        )
    else:
        weaknesses.append(
            "LinkedIn profile missing"
        )

    if quality["has_github"]:
        strengths.append(
            "GitHub profile included"
        )

    # Skills
    if len(matched_skills) >= 5:
        strengths.append(
            "Strong skill match with job description"
        )

    if len(missing_skills) >= 5:
        weaknesses.append(
            "Several important skills are missing"
        )
    
    # Sections
    for section, score in section_scores.items():

        if score >= 80:
            strengths.append(
                f"Strong {section} section"
            )

        elif score <= 40:
            weaknesses.append(
                f"Weak {section} section"
            )
    return {
        "strengths": strengths,
        "weaknesses": weaknesses
    }