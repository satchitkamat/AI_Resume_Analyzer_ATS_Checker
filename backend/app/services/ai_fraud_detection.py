from app.services.ollama_service import (
    ask_ollama
)

import json


def ai_fraud_detection(
    resume_text,
    job_description,
    github_profile,
    linkedin_profile,
    ats_score,
    matched_skills,
    missing_skills,
    candidate_validation
):

    prompt = f"""
You are an expert recruiter and hiring manager.

Resume:
{resume_text}

Job Description:
{job_description}

ATS Score:
{ats_score}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

GitHub Profile:
{github_profile}

LinkedIn Profile:
{linkedin_profile}

Candidate Validation:
{candidate_validation}

Analyze this candidate for possible resume risks.

Check:

1. Skill inflation
2. Unsupported technical claims
3. Missing proof for listed skills
4. Keyword stuffing
5. Suspicious project descriptions
6. Experience inconsistencies
7. Education inconsistencies
8. Portfolio credibility

Return ONLY valid JSON.

{{
    "risk_score": 0,
    "risk_level": "Low",
    "suspicious_claims": [],
    "verified_claims": [],
    "reasons": [],
    "recruiter_warning": ""
}}
"""

    try:

        response = ask_ollama(prompt)

        # Remove markdown if model returns ```json
        response = response.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        return json.loads(response)

    except Exception as e:

        return {

            "risk_score": 0,

            "risk_level": "Unknown",

            "suspicious_claims": [],

            "verified_claims": [],

            "reasons": [],

            "recruiter_warning":
            "AI fraud detection unavailable.",

            "error": str(e)
        }