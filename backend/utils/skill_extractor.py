import json
import os

# Get the absolute path to the current directory (backend/utils)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "software_skills.json")

def load_skills():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

SKILLS_DB = load_skills()

def extract_skills(text):
    found = set()
    text_lower = text.lower()
    for category in SKILLS_DB:
        for skill in SKILLS_DB[category]:
            # Simple check for skill in text
            if skill.lower() in text_lower:
                found.add(skill.lower())
    return list(found)

def compare_skills(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    matched = resume_set.intersection(jd_set)
    missing = jd_set - resume_set
    return list(matched), list(missing)