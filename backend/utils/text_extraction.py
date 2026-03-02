import pdfplumber
import docx

def extract_text(file):
    try:
        if file.filename.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                return " ".join([page.extract_text() or "" for page in pdf.pages])

        elif file.filename.endswith(".docx"):
            doc = docx.Document(file)
            return " ".join([p.text for p in doc.paragraphs])

        else:
            return file.read().decode("utf-8")

    except Exception as e:
        print("TEXT EXTRACTION ERROR:", e)
        return ""