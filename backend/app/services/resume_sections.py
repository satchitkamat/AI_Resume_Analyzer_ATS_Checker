import re

def detect_resume_sections(text):
    text = text.lower()

    sections = {
        "education":False,
        "experience": False,
        "porjects": False,
        "skills": False,
        "certifications": False
    }

    # Education
    if re.search(r"education|qualification|university|collage", text):
        sections["education"] = True

    # Experience
    if re.search(r"experience|work experience|employment|internship", text):
        sections["experience"] = True

    # Projects
    if re.search(r"projects|personal projects", text):
        sections["porjects"] = True

    # Skills
    if re.search(r"skills|technical skills", text):
        sections["skills"] = True

    # Certifications
    if re.search(r"certification|certifications|courses", text):
        sections["certifications"] = True

    return sections