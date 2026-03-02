from flask import Flask, request, jsonify
from utils.text_extraction import extract_text
from utils.skill_extractor import extract_skills, compare_skills, calculate_semantic_score
from utils.advisor import get_ai_advice, check_experience_gap

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        jd_text = request.form.get("job_description", "")
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400

        resume_file = request.files["resume"]
        resume_text = extract_text(resume_file)

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        matched, missing = compare_skills(resume_skills, jd_skills)
        semantic_score = calculate_semantic_score(resume_skills, jd_skills)

        # ATS score = same as semantic score (you can add small bonus for experience sections)
        ats_score = semantic_score

        job_role = jd_text[:50] if jd_text else "Target Role"
        advice = get_ai_advice(missing, job_role)
        experience_warning = check_experience_gap(resume_text, jd_text)
        if experience_warning:
            advice = experience_warning + "\n\n" + advice
            ats_score = max(ats_score - 5, 0)

        return jsonify({
            "matched_skills": matched,
            "missing_skills": missing,
            "semantic_score": semantic_score,
            "ats_score": ats_score,
            "ai_advice": advice
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)