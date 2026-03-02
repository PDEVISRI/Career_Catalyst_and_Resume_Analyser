# text_extraction.py
import pdfplumber, docx, re
from io import BytesIO

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()

def extract_from_pdf(file):
    text = ""
    file.seek(0)
    with pdfplumber.open(file.stream) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted: text += extracted + " "
    return text

def extract_from_docx(file):
    text = ""
    file.seek(0)
    doc = docx.Document(BytesIO(file.read()))
    for para in doc.paragraphs:
        text += para.text + " "
    return text

def extract_text(file):
    filename = file.filename.lower()
    if filename.endswith(".pdf"):
        text = extract_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_from_docx(file)
    elif filename.endswith(".txt"):
        file.seek(0)
        text = file.read().decode("utf-8", errors="ignore")
    else:
        return ""
    return clean_text(text)