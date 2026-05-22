from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    render_template
)

from werkzeug.utils import secure_filename

import os
import re
import json

from datetime import datetime
from fpdf import FPDF

from utils.document_processor import extract_text_from_file

from utils.llm_handler import (
    summarize_text,
    translate_text,
    answer_question
)

app = Flask(__name__)

# =========================
# CONFIG
# =========================

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
HISTORY_FILE = "history.json"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Store current uploaded document
current_document = ""


# =========================
# SAVE HISTORY
# =========================

def save_history(action_type, language, content):

    history = []

    if os.path.exists(HISTORY_FILE):

        try:

            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)

        except:
            history = []

    history.insert(0, {
        "type": action_type,
        "language": language,
        "time": str(datetime.now()),
        "content": content[:300]
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# =========================
# CREATE PDF
# =========================

def create_pdf(text, language):

    filename = f"{language}_{int(datetime.now().timestamp())}.pdf"

    filepath = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)

    # clean unsupported characters
    clean_text = text.encode(
        "latin-1",
        "replace"
    ).decode("latin-1")

    pdf.multi_cell(
        0,
        10,
        clean_text
    )

    pdf.output(filepath)

    return filepath


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# FILE UPLOAD
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    global current_document

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "error": "No selected file"
            }), 400

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        current_document = extract_text_from_file(
            filepath
        )

        if not current_document.strip():

            return jsonify({
                "error": "No readable text found"
            }), 400

        return jsonify({
            "message": "File uploaded successfully",
            "text": current_document[:3000]
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# TRANSLATE
# =========================

@app.route("/translate", methods=["POST"])
def translate():

    global current_document

    try:

        if not current_document:

            return jsonify({
                "error": "Upload document first"
            }), 400

        data = request.get_json()

        language = data.get(
            "language",
            "Hindi"
        )

        translated = translate_text(
            current_document[:1500],
            language
        )

        pdf_path = create_pdf(
            translated,
            language
        )

        save_history(
            "Translation",
            language,
            translated
        )

        return jsonify({
            "translation": translated,
            "pdf": pdf_path
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# SUMMARIZE
# =========================

@app.route("/summarize", methods=["POST"])
def summarize():

    global current_document

    try:

        if not current_document:

            return jsonify({
                "error": "Upload document first"
            }), 400

        data = request.get_json()

        language = data.get(
            "language",
            "English"
        )

        summary = summarize_text(
            current_document,
            language
        )

        pdf_path = create_pdf(
            summary,
            language
        )

        save_history(
            "Summary",
            language,
            summary
        )

        return jsonify({
            "summary": summary,
            "pdf": pdf_path
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# CHAT WITH DOCUMENT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    global current_document

    try:

        if not current_document:

            return jsonify({
                "error": "Upload document first"
            }), 400

        data = request.get_json()

        question = data.get("question")

        if not question:

            return jsonify({
                "error": "Question missing"
            }), 400

        answer = answer_question(
            current_document[:1500],
            question
        )

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# EXTRACT EMAILS + PHONES
# =========================

@app.route("/extract", methods=["POST"])
def extract():

    global current_document

    try:

        if not current_document:

            return jsonify({
                "error": "Upload document first"
            }), 400

        emails = re.findall(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            current_document
        )

        phones = re.findall(
            r'\+?\d[\d\s\-]{8,15}',
            current_document
        )

        return jsonify({
            "emails": list(set(emails)),
            "phones": list(set(phones))
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# HISTORY
# =========================

@app.route("/history", methods=["GET"])
def history():

    try:

        if not os.path.exists(HISTORY_FILE):

            return jsonify([])

        with open(HISTORY_FILE, "r") as f:

            data = json.load(f)

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# CLEAR
# =========================

@app.route("/clear", methods=["POST"])
def clear():

    global current_document

    current_document = ""

    return jsonify({
        "message": "Document cleared successfully"
    })


# =========================
# DOWNLOAD PDF
# =========================

@app.route("/download/<filename>")
def download(filename):

    path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    return send_file(
        path,
        as_attachment=True
    )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
