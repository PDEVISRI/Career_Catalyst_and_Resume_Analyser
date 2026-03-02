# advisor.py
import re

def get_ai_advice(missing_skills, job_role):
    role = job_role.strip() if job_role else "your target role"
    if not missing_skills:
        return (
            f"🎉 Great job! Your resume already aligns well with {role}.\n\n"
            "✨ Add measurable achievements.\n"
            "✨ Highlight projects and leadership.\n"
            "✨ Keep formatting professional.\n"
        )
    advice = f"💡 Suggestions to strengthen your profile for {role}:\n\n"
    for skill in missing_skills:
        advice += (
            f"🔹 Improve your knowledge in {skill}.\n"
            f"   - Build a small project using {skill}.\n"
            f"   - Take an online certification.\n"
            f"   - Add practical examples in your resume.\n\n"
        )
    advice += "📌 Additional Resume Tips:\n• Quantify achievements.\n• Use action verbs.\n• Tailor resume to each job.\n"
    return advice

def check_experience_gap(resume_text, jd_text):
    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()
    experience_pattern = r"\d+\s*(\+|-)?\s*\d*\s*years?"
    jd_requires_experience = re.search(experience_pattern, jd_lower)
    has_experience = any(k in resume_lower for k in [
        "work experience","professional experience","employment","worked at","company"
    ])
    if jd_requires_experience and not has_experience:
        return (
            "⚠️ Experience Requirement Alert:\n"
            "Resume lacks clear work experience section.\n"
            "Include internships, companies, durations, projects."
        )
    return None