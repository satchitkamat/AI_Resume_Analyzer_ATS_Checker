import re


def extract_github_username(text):

    github_patterns = [

        r"github\.com/([a-zA-Z0-9_-]+)",

        r"github\s*[:\-]?\s*([a-zA-Z0-9_-]+)"
    ]

    for pattern in github_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None


def extract_linkedin_username(text):

    linkedin_patterns = [

        r"linkedin\.com/in/([a-zA-Z0-9_-]+)",

        r"linkedin\s*[:\-]?\s*([a-zA-Z0-9_-]+)"
    ]

    for pattern in linkedin_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None