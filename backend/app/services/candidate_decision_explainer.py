import json

from app.services.ollama_service import (
    ask_ollama
)

def candidate_decision_explainer(
    ats_score,
    job_match_score,
    candidate_validation,
    risk_analysis,
    fraud_analysis,
    interview_readiness,
    hiring_recommendation
):
    prompt = f"""
You are a senior recruiter.

Explain the final hiring decision.

ATS Score:
{ats_score}

Job Match Score:
{job_match_score}

Candidate Validation:
{json.dumps(candidate_validation, indent=2)}

Risk Analysis:
{json.dumps(risk_analysis, indent=2)}

Fraud Analysis:
{json.dumps(fraud_analysis, indent=2)}

Interview Readiness:
{json.dumps(interview_readiness, indent=2)}

Hiring Recommendation:
{json.dumps(hiring_recommendation, indent=2)}

Return ONLY valid JSON.

{{
    "decision_summary": "",
    "positive_factors": [],
    "negative_factors": [],
    "key_reason": "",
    "recruiter_explanation": ""
}}

Rules:

- Maximum 5 positive factors
- Maximum 5 negative factors
- Explanation must be recruiter-friendly
- No markdown
"""

    try:

        response = ask_ollama(
            prompt
        )

        start = response.find("{")
        end = response.rfind("}") + 1

        return json.loads(
            response[start:end]
        )

    except Exception as e:

        return {

            "decision_summary":
            "Decision explanation unavailable",

            "positive_factors": [],

            "negative_factors": [],

            "key_reason":
            str(e),

            "recruiter_explanation":
            "Manual review required."
        }