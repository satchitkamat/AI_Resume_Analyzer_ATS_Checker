def analyze_linkedin(username):

    if not username:

        return {
            "verified": False,
            "score": 0,
            "profile_url": None
        }
    
    score = 50

    return {

        "verified": True,

        "score": score,

        "profile_url":
        f"https://linkedin.com/in/{username}"
    }