import requests

def analyze_github(username):

    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "followers": data["followers"],
        "following": data["following"],
        "public_repos": data["public_repos"],
        "created_at": data["created_at"],
        "profile_url": data["html_url"]
    }

def calculate_github_score(data):

    score = 0

    if data["public_repos"] >= 5:
        score += 30

    if data["public_repos"] >= 10:
        score += 20

    if data["followers"] >= 10:
        score += 20

    if data["followers"] >= 50:
        score += 30

    return min(score, 100)