import re
import json
import os
from rapidfuzz import fuzz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "software_skills.json")

def load_skills():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

SKILLS_DB = load_skills()

# Alias mapping
SKILL_ALIASES = {
    "js": "javascript",
    "javascript": "javascript",
    "react": "react.js",
    "reactjs": "react.js",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "amazon web services": "aws",
    "aws cloud": "aws"
}

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    for alias, actual in SKILL_ALIASES.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        text = re.sub(pattern, actual, text)
    return text

def extract_skills(text):
    found = set()
    normalized_text = normalize_text(text)
    for category in SKILLS_DB:
        for skill in SKILLS_DB[category]:
            skill_clean = skill.lower()
            pattern = r"\b" + re.escape(skill_clean) + r"\b"
            if re.search(pattern, normalized_text):
                found.add(skill_clean)
    return sorted(list(found))

def compare_skills(resume_skills, jd_skills):
    """
    Fuzzy compare skills and return matched/missing
    """
    matched, missing = [], []
    for jd_skill in jd_skills:
        if any(fuzz.ratio(jd_skill.lower(), r.lower()) >= 80 for r in resume_skills):
            matched.append(jd_skill)
        else:
            missing.append(jd_skill)
    return matched, missing

def calculate_semantic_score(resume_skills, jd_skills):
    """
    Percentage of JD skills present in resume
    """
    if not jd_skills:
        return 0
    matched, _ = compare_skills(resume_skills, jd_skills)
    return round((len(matched) / len(jd_skills)) * 100, 2)