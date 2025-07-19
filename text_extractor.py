import fitz
import docx
import pandas as pd
import io

def extract_text(file_bytes, filename):
    if filename.endswith(".pdf"):
        return extract_pdf(file_bytes)
    elif filename.endswith(".docx"):
        return extract_word(file_bytes)
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        return extract_excel(file_bytes)
    else:
        raise ValueError("Unsupported file type")

def extract_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return " ".join([page.get_text() for page in doc])

def extract_word(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return " ".join([p.text for p in doc.paragraphs])

def extract_excel(file_bytes):
    try:
        # Try reading as .xlsx
        df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
    except Exception:
        try:
            # Try reading as .xls
            df = pd.read_excel(io.BytesIO(file_bytes), engine="xlrd")
        except Exception as e:
            raise ValueError("File is not a valid Excel file or is corrupted.") from e
    text = "\n".join(df.astype(str).apply(' '.join, axis=1))
    return text