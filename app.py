from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import re

from utils.document_processor import extract_text_from_file
from utils.llm_handler import (
    summarize_text,
    answer_question,
    translate_text
)

app = Flask(__name__)

# =========================
# CONFIG
# =========================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store uploaded document text
current_document = ""


# =========================
# HOME PAGE
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
                "error": "No file selected"
            }), 400

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        # Extract text
        current_document = extract_text_from_file(filepath)

        if not current_document.strip():

            return jsonify({
                "error": "No readable text found in document"
            }), 400

        return jsonify({
            "message": "File uploaded successfully",
            "text": current_document[:1000]
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

        return jsonify({
            "summary": summary
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

        return jsonify({
            "translation": translated
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

        # Extract emails
        emails = re.findall(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            current_document
        )

        # Extract phone numbers
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
            current_document,
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
# CLEAR DOCUMENT
# =========================

@app.route("/clear", methods=["POST"])
def clear():

    global current_document

    current_document = ""

    return jsonify({
        "message": "Document cleared successfully"
    })


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    ) 
