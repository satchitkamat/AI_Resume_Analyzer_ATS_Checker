from app.services.ollama_service import (
    ask_ollama
)

import json

def ai_risk_detection(
resume_text,
matched_skills,
missing_skills,
github_data,
linkedin_data,
candidate_validation
):
    prompt = f"""

You are an experienced recruiter.

Analyze this candidate and identify hiring risks.

Resume:
{resume_text}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

GitHub:
{json.dumps(github_data, indent=2)}

LinkedIn:
{json.dumps(linkedin_data, indent=2)}

Candidate Validation:
{json.dumps(candidate_validation, indent=2)}

Return ONLY JSON.

{{
"risk_score": 0,
"risk_level": "",
"risk_flags": [],
"recommendation": ""
}}

Risk Level must be:

Low
Medium

High
"""

    try:
    
      response = ask_ollama(prompt)
    
      start = response.find("{")
      end = response.rfind("}") + 1
    
      return json.loads(
          response[start:end]
      )
    
    except Exception:
    
      return {
          "risk_score": 50,
          "risk_level": "Unknown",
          "risk_flags": [
              "AI risk analysis unavailable"
          ],
          "recommendation":
          "Manual review required"
      }