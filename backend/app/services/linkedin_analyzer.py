def analyze_linkedin(username):

    if not username:

        return {
            "verified": False,
            "score": 0,
            "profile_url": None
        }

    return {

        "verified": True,

        "score": 100,

        "profile_url":
        f"https://linkedin.com/in/{username}"
    }