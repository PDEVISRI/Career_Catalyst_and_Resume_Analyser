from flask import Flask, request, jsonify
from utils.text_extraction import extract_text
from utils.skill_extractor import extract_skills, compare_skills
from utils.semantic_matcher import get_similarity
from utils.advisor import get_ai_advice

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Get inputs from Streamlit
        jd_text = request.form.get("job_description", "")
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
            
        resume_file = request.files["resume"]
        
        # 1. Process Text
        resume_text = extract_text(resume_file)
        
        # 2. Skill Extraction
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        matched, missing = compare_skills(resume_skills, jd_skills)
        
        # 3. Semantic Analysis
        similarity = get_similarity(resume_text, jd_text)
        
        # 4. Scoring (60% Keywords, 40% Semantic)
        keyword_score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 0
        final_score = round((keyword_score * 0.6) + (similarity * 100 * 0.4), 2)

        # 5. Get AI Advice (Hugging Face)
        advice = get_ai_advice(resume_text, jd_text, missing)

        return jsonify({
            "matched_skills": matched,
            "missing_skills": missing,
            "semantic_score": round(similarity * 100, 2),
            "ats_score": final_score,
            "ai_advice": advice
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)