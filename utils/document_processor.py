import os
import fitz
import pytesseract

from PIL import Image
from pdf2image import convert_from_path
from docx import Document


# =========================================
# EXTRACT TEXT
# =========================================

def extract_text_from_file(filepath):

    try:

        ext = os.path.splitext(filepath)[1].lower()

        # =====================================
        # TXT FILE
        # =====================================

        if ext == ".txt":

            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                return f.read()

        # =====================================
        # DOCX FILE
        # =====================================

        elif ext == ".docx":

            doc = Document(filepath)

            text = []

            for para in doc.paragraphs:

                text.append(para.text)

            return "\n".join(text)

        # =====================================
        # PDF FILE
        # =====================================

        elif ext == ".pdf":

            text = ""

            # TRY NORMAL PDF EXTRACTION FIRST
            pdf_document = fitz.open(filepath)

            for page_num in range(len(pdf_document)):

                page = pdf_document[page_num]

                extracted = page.get_text("text")

                text += extracted

            pdf_document.close()

            # IF TEXT IS VALID
            if len(text.strip()) > 50:

                return text

            # =====================================
            # OCR FOR SCANNED PDF
            # =====================================

            print("Using OCR extraction...")

            images = convert_from_path(filepath)

            ocr_text = ""

            for image in images:

                extracted_text = pytesseract.image_to_string(image)

                ocr_text += extracted_text + "\n"

            return ocr_text

        else:

            return "Unsupported file format"

    except Exception as e:

        return f"Extraction Error: {str(e)}"
