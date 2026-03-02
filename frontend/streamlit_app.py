import streamlit as st
import requests
from io import BytesIO
import PyPDF2
import docx

# Page Settings
st.set_page_config(page_title="Career Catalyst | Resume Analyser", layout="wide")

# Custom CSS for the "Career Catalyst" Dark Style
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #ffffff; }
    
    .main-title {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 20px;
        margin-top: -5px;
        margin-bottom: 30px;
    }

    .section-header {
        color: #f1f5f9;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
    }

    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
        height: 3.5em;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3b82f6;
        box-shadow: 0px 0px 15px rgba(59, 130, 246, 0.4);
    }

    .skill-badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        background-color: #1e293b;
        color: #3b82f6;
        border: 1px solid #334155;
        font-weight: 500;
    }
    
    .advice-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #2563eb;
        color: #e2e8f0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper for UI text extraction
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
st.markdown('<p class="sub-title">Resume Analyser</p>', unsafe_allow_html=True)
st.divider()

# Inputs
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<p class="section-header">📄 Job Description</p>', unsafe_allow_html=True)
    jd_input = st.text_area("JD", height=400, placeholder="Paste JD here...", label_visibility="collapsed")

with col_right:
    st.markdown('<p class="section-header">📝 Resume Content</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload", type=["pdf", "docx"], label_visibility="collapsed")
    
    # Auto-extract text if file is uploaded
    display_text = ""
    if uploaded_file:
        display_text = extract_ui_text(uploaded_file)
    
    st.markdown("<p style='text-align: center; color: #64748b; margin: 5px 0;'>— OR PASTE BELOW —</p>", unsafe_allow_html=True)
    resume_input = st.text_area("Resume", value=display_text, height=245, placeholder="Resume text will appear here...", label_visibility="collapsed")

# Actions
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

# Results
if 'results' in st.session_state:
    res = st.session_state['results']
    st.markdown("---")
    st.markdown("### 📊 Analysis Dashboard")
    
    m1, m2 = st.columns(2)
    m1.metric("Overall ATS Score", f"{res['ats_score']}%")
    m2.metric("Semantic Match", f"{res['semantic_score']}%")
    
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<p class="section-header">✅ Matched Skills</p>', unsafe_allow_html=True)
        if res['matched_skills']:
            badges = "".join([f'<span class="skill-badge">{s}</span>' for s in res['matched_skills']])
            st.markdown(badges, unsafe_allow_html=True)
            
    with r2:
        st.markdown('<p class="section-header">❌ Missing Skills</p>', unsafe_allow_html=True)
        if res['missing_skills']:
            badges = "".join([f'<span class="skill-badge" style="color:#f87171;">{s}</span>' for s in res['missing_skills']])
            st.markdown(badges, unsafe_allow_html=True)

    # Advisor Section
    st.markdown("---")
    st.markdown("### 💡 Career Catalyst Advisor")
    st.markdown(f'<div class="advice-box">{res.get("ai_advice", "No advice available.")}</div>', unsafe_allow_html=True)