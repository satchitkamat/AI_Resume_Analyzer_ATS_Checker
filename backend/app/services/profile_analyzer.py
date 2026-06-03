from app.services.profile_extractor import (
    extract_github_username,
    extract_linkedin_username
)

from app.services.github_analyzer import (
    analyze_github,
    calculate_github_score
)

from app.services.linkedin_analyzer import (
    analyze_linkedin
)
from app.services.github_repo_analyzer import (
    get_github_repositories,
    extract_repo_languages,
    calculate_github_skill_match,
    calculate_repo_quality,
    detect_repo_topics,
    extract_repo_technologies
)


def analyze_profiles(resume_text,job_skills):

    github_username = extract_github_username(
        resume_text
    )

    linkedin_username = extract_linkedin_username(
        resume_text
    )

    github_data = None
    github_score = 0
    repos = []
    repo_languages = []

    if github_username:

        github_data = analyze_github(
            github_username
        )

        if github_data:

            github_score = calculate_github_score(
                github_data
            )
           
            
        repos = get_github_repositories(
            github_username
        )

        repo_languages = extract_repo_languages(
            repos
        )

        repo_topics = detect_repo_topics(
            repos
        )

        repo_technologies = extract_repo_technologies(
            repos
        )

        print("Repo Technologies:", repo_technologies)
        print("Job Skills:", job_skills)

    linkedin_data = {
        "verified": False,
        "score": 0,
        "profile_url": None
    }

    if linkedin_username:
        linkedin_data = analyze_linkedin(
            linkedin_username
        )

    

    github_skill_match_score = 0
    matched_repo_skills = []
    repo_quality_score = 0

    if job_skills:
        
        github_skill_match_score, matched_repo_skills = (
            calculate_github_skill_match(
                repo_languages,
                job_skills
            )
        )

    repo_quality_score = calculate_repo_quality(
        repos
    )

    return {

        "github": {

            "username": github_username,
        
            "verified": github_data is not None,
        
            "score": github_score,
        
            "followers": github_data["followers"]
            if github_data else 0,
        
            "public_repos": github_data["public_repos"]
            if github_data else 0,
        
            "languages": repo_languages,

            "repo_topics": repo_topics,

            "repo_technologies": repo_technologies,
        
            "repo_quality_score":
            repo_quality_score,
        
            "github_skill_match":
            github_skill_match_score,
        
            "matched_repo_skills":
            matched_repo_skills
        },

        "linkedin": {
            "username": linkedin_username,
            "verified": linkedin_data["verified"],
            "score": linkedin_data["score"],
            "profile_url": linkedin_data["profile_url"]
        }
    }