from app.services.ollama_service import (
    ask_ollama
)

import json

def ai_hiring_recommendation(
    ats_score,
    job_match_score,
    candidate_validation,
    github_score,
    linkedin_score
):
    prompt = f"""

You are a senior hiring manager.

Analyze the candidate data below and make a hiring recommendation.

ATS Score:
{ats_score}

Job Match Score:
{job_match_score}

GitHub Score:
{github_score}

LinkedIn Score:
{linkedin_score}

Candidate Validation:
{json.dumps(candidate_validation, indent=2)}

Return ONLY JSON.

{{
"decision": "",
"confidence": "",
"reason": "",
"next_action": ""
}}

Decision must be one of:

Strong Hire
Hire
Interview
Hold
Reject

Confidence must be:

High
Medium

Low
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
    
    except Exception:
    
      return {
          "decision": "Manual Review",
          "confidence": "Low",
          "reason": "AI recommendation unavailable",
          "next_action": "Review manually"
      }