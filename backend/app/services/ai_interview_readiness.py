import json 

from app.services.ollama_service import (
    ask_ollama
)
import re

def ai_interview_readiness(
    resume_text,
    ats_score,
    job_match_score,
    candidate_validation,
    risk_analysis
):
    prompt = f"""
You are a senior recruiter and hiring manager.

Determine whether this candidate is ready for an interview.

Analyze:

1. Resume quality
2. ATS score
3. Job match score
4. Skill evidence
5. Candidate validation
6. Hiring risks
7. Technical depth
8. Communication quality

ATS Score:
{ats_score}

Job Match Score:
{job_match_score}

Candidate Validation:
{json.dumps(candidate_validation, indent=2)}

Risk Analysis:
{json.dumps(risk_analysis, indent=2)}

Resume:
{resume_text}

Return ONLY valid JSON.

{{
    "interview_readiness_score": 0,
    "readiness_level": "",
    "recommended_interview_type": "",
    "likely_strengths": [],
    "potential_gaps": [],
    "recruiter_notes": ""
}}

Rules:

readiness_level must be:

Low
Medium
High

recommended_interview_type must be:

HR
Technical
Technical + HR
Managerial
Not Recommended
"""
    
    try:

        response = ask_ollama(prompt)

        match = re.search(
            r'\{[\s\S]*\}',
            response
        )

        if not match:
            raise Exception("No JSON found")

        json_text = match.group(0)


        return json.loads(json_text)
    
    except Exception as e:


        return {

            "interview_readiness_score": 0,

            "readiness_level":
            "Unknown",

            "recommended_interview_type":
            "Manual Review",

            "likely_strengths": [],

            "potential_gaps": [],

            "recruiter_notes":
            f"AI interview readiness unavailable: {str(e)}"
        }