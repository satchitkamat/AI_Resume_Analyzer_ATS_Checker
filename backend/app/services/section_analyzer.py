import re 

def extract_sections(text):

    sections = {
        "education": "",
        "skills": "",
        "projects": "",
        "experience": "",
        "summary": "",
    }

    text_lower = text.lower()

    pattern = {
        "education": r"education(.*?)(skills|projects|experience|$)",
        "skills": r"skills(.*?)(education|projects|experience|$)",
        "projects": r"projects(.*?)(education|skills|experience|$)",
        "experience": r"experience(.*?)(education|skills|projects|$)",
        "summary": r"(summary|objective)(.*?)(education|skills|projects|experience|$)"
    }

    for section, pattern in pattern.items():

        match = re.search(
            pattern,
            text_lower,
            re.DOTALL
        )

        if match:
            sections[section] = match.group(1)

    return sections

def score_sections(sections):
    
    scores = {}

    for section, content in sections.items():

        word_count = len(content.split())

        if word_count > 100:
            scores[section] = 100

        elif word_count > 50:
            scores[section] = 80

        elif word_count > 20:
            scores[section] = 60

        elif word_count > 0:
            scores[section] = 40

        else:
            scores[section] = 0

    return scores