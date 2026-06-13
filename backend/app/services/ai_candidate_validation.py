import json

from app.services.ollama_service import (
ask_ollama
)

def ai_candidate_validation(
    resume_text,
    github_data,
    linkedin_data,
    ats_score,
    matched_skills,
    missing_skills,
    job_match_score,
    section_scores
):

    prompt = f"""


You are a senior recruiter and hiring manager.

Analyze this candidate using:

1. Resume
2. GitHub Profile
3. LinkedIn Profile
4. ATS Analysis

Your goal is to help recruiters decide whether this candidate should move forward in the hiring process.

Evaluate:

* Candidate credibility
* Skill verification
* Resume quality
* GitHub evidence
* LinkedIn evidence
* Job fit
* Hiring confidence
* Hiring risks
* Interview recommendation

Return ONLY valid JSON.

ATS SCORE:
{ats_score}

JOB MATCH SCORE:
{job_match_score}

MATCHED SKILLS:
{matched_skills}

MISSING SKILLS:
{missing_skills}

SECTION SCORES:
{json.dumps(section_scores, indent=2)}

GITHUB DATA:
{json.dumps(github_data, indent=2)}

LINKEDIN DATA:
{json.dumps(linkedin_data, indent=2)}

RESUME:
{resume_text}

Return JSON in this exact format:

{{
"credibility_score": 0,
"job_fit_score": 0,
"hiring_confidence": "",
"interview_recommendation": "",
"interview_chance": "",
"verified_claims": [],
"questionable_claims": [],
"risk_flags": [],
"strengths": [],
"concerns": [],
"recruiter_summary": ""
}}
"""

    try:
    
        response = ask_ollama(
            prompt
        )
    
        start = response.find("{")
        end = response.rfind("}") + 1
    
        if start == -1 or end == 0:
            raise Exception(
                "No valid JSON found in AI response"
            )
    
        ai_result = json.loads(
            response[start:end]
        )
    
        return ai_result
    
    except Exception as e:
    
        return {
        
            "credibility_score": 0,
    
            "job_fit_score": 0,
    
            "hiring_confidence":
            "Unknown",
    
            "interview_recommendation":
            "Manual Review",
    
            "interview_chance":
            "Unknown",
    
            "verified_claims": [],
    
            "questionable_claims": [],
    
            "risk_flags": [
                str(e)
            ],
    
            "strengths": [],
    
            "concerns": [],
    
            "recruiter_summary":
            "AI candidate validation unavailable."
        }