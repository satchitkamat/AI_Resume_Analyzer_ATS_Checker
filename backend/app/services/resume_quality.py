import re


def analyze_resume_quality(text):

    results = {}

    # word count
    words = text.split()

    word_count = len(words)

    results["word_count"] = word_count

    # Resume length quality
    if word_count < 200:

        results["resume_length"] = "Too Short"

    elif word_count > 1200:

        results["resume_length"] = "Too long"

    else:

        results["resume_length"] = "Good"

    # Email detection
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    results["email_found"] = bool(
        re.search(email_pattern,text)
    )

    # Phone number
    phone_pattern = r"\+?\d[\d -]{8,}\d"
    results["phone_found"]= bool(
        re.search(phone_pattern, text)
    )
    

    
    # LinkedIn detection
    results["linkedin_found"] = (
        "linkedin.com" in text.lower()
        or "linkedin" in text.lower()
    )

    # GitHub detection
    results["github_found"] = (
        "github.com" in text.lower()
        or "github" in text.lower()
    )

    return results