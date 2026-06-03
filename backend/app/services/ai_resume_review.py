from app.services.ollama_service import ask_ollama
import json

def ai_resume_review(
    resume_text,
    job_description
):
    prompt = f"""
Analyze this resume against the job description.

Return ONLY valid JSON.

Format:

{{
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "project_improvements": {{
      "MiniCodeHub": [],
      "AI Resume Analyzer": []
  }},
  "action_items": []
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""
    
    response = ask_ollama(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "error": "AI response parsing failed"
        }