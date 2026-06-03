import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.resume_sections import detect_resume_sections
from app.services.resume_parser import extract_resume_sections
from app.services.ai_feedback import generate_ai_feedback
from app.services.section_analyzer import extract_sections, score_sections
from app.services.resume_insights import get_resume_insights
from app.services.profile_analyzer import (
    analyze_profiles
)

from app.services.ai_resume_review import (
    ai_resume_review
)

from app.services.job_match_service import (
    calculate_job_match,
    get_job_match_feedback
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

    suggestions = generate_suggestions(
        quality
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

    job_match_feedback = get_job_match_feedback(
        job_match_score
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

    # =====================
    # AI Feedback
    # =====================

    ai_feedback = generate_ai_feedback(
        ats_score,
        matched_skills,
        missing_skills,
        suggestions
    )

    # =====================
    # Insights
    # =====================

    insights = get_resume_insights(
        quality,
        matched_skills,
        missing_skills,
        section_scores
    )

    ai_analysis = ai_resume_review(
        resume_text,
        job_description,
    )

    # =====================
    # Response
    # =====================

    return {

        "ats_score": ats_score,

        "matched_skills":
        matched_skills,

        "missing_skills":
        missing_skills,

        "quality":
        quality,

        "suggestions":
        suggestions,

        "ai_feedback":
        ai_feedback,

        "section_scores":
        section_scores,

        "strengths":
        insights["strengths"],

        "weaknesses":
        insights["weaknesses"],

        "profiles":
        profiles,

        "score_breakdown": {

            "similarity_score":
            similarity_score,

            "skill_match_score":
            round(
                skill_match_score,
                2
            ),

            "section_score":
            section_score,

            "profile_score":
            round(
                profile_score,
                2
            )
        },
        "job_match": {

            "score": job_match_score,

            "status":
            job_match_feedback["status"],

            "interview_chance":
            job_match_feedback["chance"]
        },
        

        "ai_analysis": ai_analysis
    }