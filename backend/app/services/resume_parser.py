import re


def extract_resume_sections(text: str):

    sections = {
        "education": "",
        "experience": "",
        "skills": "",
        "projects": "",
        "certifications": ""
    }

    text_lower = text.lower()

    patterns = {
        "education": r"education(.*?)(experience|skills|projects|certifications|$)",

        "experience": r"experience(.*?)(education|skills|projects|certifications|$)",

        "skills": r"skills(.*?)(education|experience|projects|certifications|$)",

        "projects": r"projects(.*?)(education|experience|skills|certifications|$)",

        "certifications": r"certifications(.*?)(education|experience|skills|projects|$)"
    }

    for section, pattern in patterns.items():

        match = re.search(
            pattern,
            text_lower,
            re.DOTALL
        )

        if match:

            sections[section] = match.group(1).strip()

    return sections