import os
import fitz
from docx import Document


def extract_text_from_file(filepath):

    try:

        ext = os.path.splitext(filepath)[1].lower()

        # =========================
        # TXT FILE
        # =========================

        if ext == ".txt":

            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                return f.read()

        # =========================
        # PDF FILE
        # =========================

        elif ext == ".pdf":

            text = ""

            pdf_document = fitz.open(filepath)

            for page_num in range(len(pdf_document)):

                page = pdf_document[page_num]

                text += page.get_text("text")

            pdf_document.close()

            return text.strip()

        # =========================
        # DOCX FILE
        # =========================

        elif ext == ".docx":

            doc = Document(filepath)

            text = []

            for para in doc.paragraphs:

                text.append(para.text)

            return "\n".join(text)

        else:

            return "Unsupported file format"

    except Exception as e:

        return f"Extraction Error: {str(e)}"
