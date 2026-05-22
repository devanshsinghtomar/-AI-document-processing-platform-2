import os
import fitz  # PyMuPDF
from docx import Document


# =========================================
# EXTRACT TEXT FROM FILE
# =========================================

def extract_text_from_file(filepath):

    try:

        ext = os.path.splitext(filepath)[1].lower()

        # =====================
        # TXT FILE
        # =====================

        if ext == ".txt":

            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                return file.read()

        # =====================
        # PDF FILE
        # =====================

        elif ext == ".pdf":

            text = ""

            pdf = fitz.open(filepath)

            for page in pdf:

                text += page.get_text()

            pdf.close()

            return text.strip()

        # =====================
        # DOCX FILE
        # =====================

        elif ext == ".docx":

            doc = Document(filepath)

            full_text = []

            for para in doc.paragraphs:

                full_text.append(para.text)

            return "\n".join(full_text)

        else:

            return "Unsupported file format."

    except Exception as e:

        return f"File Processing Error: {str(e)}"
