import os
import pytesseract
from pdf2image import convert_from_path
import pdfplumber
import docx

def extract_text_from_pdf(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        # pdfplumber ile okunmazsa OCR'a düş
        pages = convert_from_path(path, dpi=300)
        for page in pages:
            text += pytesseract.image_to_string(page, lang='tur') + "\n"
    return text.strip()

def extract_text_from_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        return ""

def extract_text_from_txt(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        return ""

def extract_text_from_image(path):
    try:
        return pytesseract.image_to_string(path, lang='tur').strip()
    except Exception as e:
        return ""

def extract_text_from_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(path)
    elif ext == '.docx':
        return extract_text_from_docx(path)
    elif ext == '.txt':
        return extract_text_from_txt(path)
    elif ext in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(path)
    else:
        return "Desteklenmeyen dosya türü"

