import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(filepath):

    ext = os.path.splitext(filepath)[1].lower()

    text = ""

    try:

        # TXT
        if ext == ".txt":

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        # PDF
        elif ext == ".pdf":

            reader = PdfReader(filepath)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        # DOCX
        elif ext == ".docx":

            doc = Document(filepath)

            for para in doc.paragraphs:
                text += para.text + "\n"

        return text.strip()

    except Exception as e:

        return f"Error extracting text: {str(e)}"
