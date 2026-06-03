import requests
from collections import Counter

def get_github_repositories(username):

    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    return response.json()

def extract_repo_languages(repos):
    languages = []

    for repo in repos:


        if repo["language"]:
            languages.append(
                repo["language"].lower()
            )

    return list(set(languages))


def calculate_github_skill_match(repo_technologies, job_skills):

    matched = []
    print("Repo Technologies:", repo_technologies)
    print("Job Skills:", job_skills)
    

    for skill in job_skills:

        print("Checking:", skill)

        if skill.lower() in [
            tech.lower()
            for tech in repo_technologies
        ]:
            matched.append(skill)

    matched_skills = list(
        set(repo_technologies)
        &
        set(job_skills)
    )

    print("Matched:", matched_skills)

    score = (
        len(matched) /
        len(job_skills) * 100
    ) if job_skills else 0

    return round(score, 2), matched

def calculate_repo_quality(repos):

    score = 0

    repo_count = len(repos)

    if repo_count >= 3:
        score += 20

    if repo_count >= 5:
        score += 20

    if repo_count >= 10:
        score += 20

    total_stars = sum(
        repo["stargazers_count"]
        for repo in repos
    )

    if total_stars >= 5:
        score += 20

    if total_stars >= 20:
        score += 20

    return min(score, 100)

def detect_repo_topics(repos):

    skills = []

    for repo in repos:

        topics = repo.get(
            "tpoics",
            []
        )

        for topic in topics:
            skills.append(
                topic.lower()
            )

    return list(set(skills))

def extract_repo_technologies(repos):

    technologies = set()

    for repo in repos:

        text = (
            f"{repo.get('name', '')} "
            f"{repo.get('description', '')}"
        ).lower()

        if "react" in text:
            technologies.add("react")

        if "next" in text:
            technologies.add("next.js")

        if "tailwind" in text:
            technologies.add("tailwind css")

        if "node" in text:
            technologies.add("node.js")

        if "fastapi" in text:
            technologies.add("fastapi")

        if "python" in text:
            technologies.add("python")

        if "javascript" in text:
            technologies.add("javascript")

        if "typescript" in text:
            technologies.add("typescript")

        if "html" in text:
            technologies.add("html")

        if "css" in text:
            technologies.add("css")

        if "c++" in text or "cplusplus" in text:
            technologies.add("c++")

        if "mysql" in text:
            technologies.add("mysql")

        if "mongodb" in text:
            technologies.add("mongodb")

        if "docker" in text:
            technologies.add("docker")

        if "git" in text:
            technologies.add("git")

    return list(technologies)