# utils/semantic_matcher.py

from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_similarity(resume_sections: list, jd_text: str) -> float:
    """
    Compute semantic similarity between JD and each resume section.
    Returns average similarity (0.0 - 1.0)
    """
    try:
        jd_embedding = model.encode(jd_text, convert_to_tensor=True)
        scores = []
        for section in resume_sections:
            sec_embedding = model.encode(section, convert_to_tensor=True)
            cosine_score = util.pytorch_cos_sim(sec_embedding, jd_embedding)
            scores.append(float(cosine_score.item()))
        
        if scores:
            avg_score = sum(scores) / len(scores)
            return avg_score
        return 0.0
    except Exception as e:
        print("Error in semantic matching:", e)
        return 0.0

def split_resume_sections(resume_text: str) -> list:
    """
    Extract sections like SKILLS, PROJECTS, EDUCATION for better semantic matching
    """
    sections = []
    for heading in ["SKILLS", "PROJECTS", "EDUCATION", "CERTIFICATIONS", "LEADERSHIP"]:
        pattern = r"{}(.*?)(?=SKILLS|PROJECTS|EDUCATION|CERTIFICATIONS|LEADERSHIP|$)".format(heading)
        match = re.search(pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if match:
            sections.append(match.group(1).strip())
    return sections