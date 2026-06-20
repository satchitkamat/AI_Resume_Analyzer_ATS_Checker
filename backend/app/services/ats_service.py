import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.resume_sections import detect_resume_sections
from app.services.resume_parser import extract_resume_sections
from app.services.section_analyzer import extract_sections, score_sections
from app.services.resume_insights import get_resume_insights
from app.services.profile_analyzer import (
    analyze_profiles
)

from app.services.job_match_service import (
    calculate_job_match
)

from app.services.ai_candidate_validation import (
    ai_candidate_validation
)

from app.services.ai_hiring_recommendation import (
    ai_hiring_recommendation
)

from app.services.ai_risk_detection import (
    ai_risk_detection
)

from app.services.ai_interview_readiness import (
    ai_interview_readiness
)
from app.services.ai_fraud_detection import (
    ai_fraud_detection
)

from app.services.candidate_analysis_service import (
    save_candidate_analysis
)

from app.services.pipeline import (
    create_pipeline_entry
)

def clean_text(text):
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    return text


def extract_skills(text):
    """
    Extract skills from comma-separated Job Description input.
    Example:
    python,c++,html,css,node.js
    """

    return [
        skill.strip().lower()
        for skill in text.split(",")
        if skill.strip()
    ]


def match_skills(job_description, resume_text):

    jd_skills = extract_skills(job_description)

    resume_text = resume_text.lower()

    matched_skills = []
    missing_skills = []

    for skill in jd_skills:

        if skill.lower() in resume_text:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


def analyze_resume_quality(text):

    results = {}

    results["word_count"] = len(text.split())

    results["has_email"] = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
    )

    results["has_phone"] = bool(
        re.search(
            r"\+?\d[\d\s\-]{8,15}",
            text
        )
    )

    results["has_linkedin"] = (
        "linkedin.com" in text.lower()
        or "linkedin" in text.lower()
    )

    results["has_github"] = (
        "github.com" in text.lower()
        or "github" in text.lower()
    )

    return results


def generate_suggestions(quality):

    suggestions = []

    if not quality["has_email"]:
        suggestions.append("Add an email address")

    if not quality["has_phone"]:
        suggestions.append("Add a phone number")

    if not quality["has_linkedin"]:
        suggestions.append("Add a LinkedIn profile")

    if not quality["has_github"]:
        suggestions.append("Add a GitHub profile")

    if quality["word_count"] < 250:
        suggestions.append(
            "Resume appears too short. Add more project and experience details."
        )

    return suggestions


def calculate_ats_score(
    db,
    resume,
    resume_text,
    job_description
):

    # =====================
    # Text Cleaning
    # =====================

    cleaned_resume = clean_text(
        resume_text
    )

    cleaned_jd = clean_text(
        job_description
    )

    # =====================
    # TF-IDF Similarity
    # =====================

    documents = [
        cleaned_resume,
        cleaned_jd
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        matrix
    )[0][1]

    similarity_score = round(
        similarity * 100,
        2
    )

    # =====================
    # Skill Matching
    # =====================

    matched_skills, missing_skills = (
        match_skills(
            job_description,
            resume_text
        )
    )


    print("Matched Skills:", matched_skills)
    print("Missing Skills:", missing_skills)

    job_skills = extract_skills(
        job_description
    )

    if len(job_skills) > 0:

        skill_match_score = (
            len(matched_skills)
            / len(job_skills)
        ) * 100

    else:

        skill_match_score = 0

    # =====================
    # Resume Quality
    # =====================

    quality = analyze_resume_quality(
        resume_text
    )

    # =====================
    # Resume Sections
    # =====================

    detect_resume_sections(
        resume_text
    )

    extract_resume_sections(
        resume_text
    )

    sections = extract_sections(
        resume_text
    )

    section_scores = score_sections(
        sections
    )

    if section_scores:

        section_score = round(
            sum(
                section_scores.values()
            )
            /
            len(section_scores),
            2
        )

    else:

        section_score = 0

    # =====================
    # Profile Analysis
    # =====================

    profiles = analyze_profiles(
        resume_text,
        job_skills
    )

    github_technologies = profiles[
        "github"
    ]["repo_technologies"]

    github_score = profiles[
        "github"
    ]["score"]

    linkedin_score = profiles[
        "linkedin"
    ]["score"]

    github_skill_match = profiles[
        "github"
    ]["github_skill_match"]

    profile_score = (
        github_score +
        linkedin_score
    ) / 2

    job_match_score = calculate_job_match(
        ats_score=skill_match_score,
        github_skill_match=github_skill_match,
        github_score=github_score,
        section_score=section_score
    )

    # =====================
    # Final ATS Score
    # =====================

    ats_score = round(

        (
            skill_match_score * 0.50
            +
            section_score * 0.15
            +
            profile_score * 0.15
            +
            similarity_score * 0.20
        ),

        2
    )

    candidate_validation = ai_candidate_validation(
        resume_text=resume_text,
        github_data=profiles["github"],
        linkedin_data=profiles["linkedin"],
        ats_score=ats_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        job_match_score=job_match_score,
        section_scores=section_scores
    )

    hiring_recommendation = (
        ai_hiring_recommendation(
            ats_score=ats_score,
            job_match_score=job_match_score,
            candidate_validation=candidate_validation,
            github_score=github_score,
            linkedin_score=linkedin_score
        )
    )

    risk_analysis = ai_risk_detection(
        resume_text=resume_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        github_data=profiles["github"],
        linkedin_data=profiles["linkedin"],
        candidate_validation=candidate_validation
    )

    interview_readiness = (
        ai_interview_readiness(

            resume_text,

            ats_score,

            job_match_score,

            candidate_validation,

            risk_analysis
        )
    )
    fraud_analysis = (
        ai_fraud_detection(
            resume_text=resume_text,
            job_description=job_description,
            github_profile=profiles["github"],
            linkedin_profile=profiles["linkedin"],
            ats_score=ats_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            candidate_validation=candidate_validation
        )
    )

    save_candidate_analysis(

        db=db,
    
        resume_id=resume.id,
    
        ats_score=ats_score,
    
        candidate_validation=
        candidate_validation,
    
        risk_analysis=
        risk_analysis,
    
        interview_readiness=
        interview_readiness,
    
        hiring_recommendation=
        hiring_recommendation
    )

    create_pipeline_entry(
        db,
        resume.id
    )
    # =====================
    # Response
    # =====================

    return {

        "ats_score": ats_score,

        "matched_skills":matched_skills,

        "missing_skills":missing_skills,

        "section_scores":section_scores,

        "profiles":profiles,

        "score_breakdown": {

            "similarity_score":similarity_score,

            "skill_match_score":
            round(
                skill_match_score,
                2
            ),

            "section_score":section_score,

            "profile_score":
            round(
                profile_score,
                2
            )
        },
        "candidate_validation":candidate_validation,

        "hiring_recommendation":hiring_recommendation,

        "risk_analysis":risk_analysis,

        "interview_readiness":interview_readiness,

        "fraud_analysis": fraud_analysis,

    }