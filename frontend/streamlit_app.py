import streamlit as st
import requests
from io import BytesIO
import PyPDF2
import docx

# Page Settings
st.set_page_config(page_title="Career Catalyst | Resume Analyzer", layout="wide")

# Custom CSS for modern dark theme with bigger text
st.markdown("""
<style>
.stApp { background-color: #0f172a; color: #ffffff; }

.main-title { color: #ffffff; font-size: 52px; font-weight: 800; margin-bottom: 0px; }
.sub-title { color: #94a3b8; font-size: 28px; margin-top: -5px; margin-bottom: 30px; }  /* increased */
.section-header { color: #f1f5f9; font-size: 24px; font-weight: 600; margin-bottom: 12px; } /* increased */

.stTextArea textarea { background-color: #1e293b !important; color: #ffffff !important; border: 1px solid #334155 !important; border-radius: 12px; font-size: 18px !important; } /* increased */
.stButton>button { background-color: #2563eb; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 3.5em; border: none; font-size: 18px; } /* increased */
.stButton>button:hover { background-color: #3b82f6; box-shadow: 0px 0px 15px rgba(59, 130, 246, 0.4); }

.skill-card { display: inline-block; padding: 10px 18px; margin: 4px; border-radius: 12px; font-weight: 500; font-size: 18px; } /* bigger */
.matched { background-color: #1e293b; color: #10b981; border: 1px solid #064e3b; }
.missing { background-color: #1e293b; color: #f87171; border: 1px solid #7f1d1d; }

.advice-box { background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #2563eb; color: #e2e8f0; line-height: 1.8; font-size: 18px; } /* bigger */
.progress-bar { height: 35px; border-radius: 12px; background-color: #334155; } /* taller */
.progress-fill { height: 100%; border-radius: 12px; background-color: #2563eb; text-align: center; font-weight: bold; color: white; line-height: 35px; font-size: 18px; } /* bigger */
</style>
""", unsafe_allow_html=True)

# Helper to extract text from PDF/DOCX
def extract_ui_text(file):
    text = ""
    try:
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(BytesIO(file.getvalue()))
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(BytesIO(file.getvalue()))
            text = "\n".join([p.text for p in doc.paragraphs])
    except:
        pass
    return text

# Header
st.markdown('<p class="main-title">Career Catalyst</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Resume Analyzer</p>', unsafe_allow_html=True)
st.divider()

# Input columns
col_left, col_right = st.columns(2)
with col_left:
    st.markdown('<p class="section-header">📄 Job Description</p>', unsafe_allow_html=True)
    jd_input = st.text_area("JD", height=400, placeholder="Paste JD here...", label_visibility="collapsed")

with col_right:
    st.markdown('<p class="section-header">📝 Resume Content</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], label_visibility="collapsed")
    
    display_text = ""
    if uploaded_file:
        display_text = extract_ui_text(uploaded_file)
    
    st.markdown("<p style='text-align: center; color: #64748b;'>— OR PASTE BELOW —</p>", unsafe_allow_html=True)
    resume_input = st.text_area("Resume Text", value=display_text, height=245, placeholder="Resume text will appear here...", label_visibility="collapsed")

# Action buttons
st.divider()
_, _, scan_col, clear_col = st.columns([4, 4, 1.5, 1.5])

with scan_col:
    if st.button("SCAN RESUME"):
        if resume_input and jd_input:
            with st.spinner("Analyzing..."):
                files = {"resume": ("resume.txt", resume_input, "text/plain")}
                data = {"job_description": jd_input}
                try:
                    r = requests.post("http://127.0.0.1:5000/analyze", files=files, data=data)
                    if r.status_code == 200:
                        st.session_state['results'] = r.json()
                        st.success("Analysis Complete!")
                    else:
                        st.error("Backend Error.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please provide both documents.")

with clear_col:
    if st.button("CLEAR"):
        st.session_state.clear()
        st.rerun()

# Display results
if 'results' in st.session_state:
    res = st.session_state['results']
    st.markdown("---")
    st.markdown("### 📊 Analysis Dashboard")
    
    # Scores with progress bars
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Overall ATS Score**")
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width:{res['ats_score']}%;">{res['ats_score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("**Semantic Match**")
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width:{res['semantic_score']}%;">{res['semantic_score']}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Skills
    st.markdown("---")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<p class="section-header">✅ Matched Skills</p>', unsafe_allow_html=True)
        if res['matched_skills']:
            badges = "".join([f'<span class="skill-card matched">{s}</span>' for s in res['matched_skills']])
            st.markdown(badges, unsafe_allow_html=True)
    with r2:
        st.markdown('<p class="section-header">❌ Missing Skills</p>', unsafe_allow_html=True)
        if res['missing_skills']:
            badges = "".join([f'<span class="skill-card missing">{s}</span>' for s in res['missing_skills']])
            st.markdown(badges, unsafe_allow_html=True)

    # Advisor (collapsible)
    st.markdown("---")
    with st.expander("💡 Career Catalyst Advisor"):
        st.markdown(f'<div class="advice-box">{res.get("ai_advice", "No advice available.")}</div>', unsafe_allow_html=True)