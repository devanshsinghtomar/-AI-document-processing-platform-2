from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from utils.document_processor import extract_text_from_file
from utils.llm_handler import (
    translate_text,
    summarize_text,
)

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
HISTORY_FILE = "history/history.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs("history", exist_ok=True)

current_document = ""


@app.route("/")
def home():
    return render_template("index.html")


# UPLOAD
@app.route("/upload", methods=["POST"])
def upload():

    global current_document

    try:

        file = request.files["file"]

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        current_document = extract_text_from_file(filepath)

        return jsonify({
            "success": True,
            "text": current_document
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


# TRANSLATE
@app.route("/translate", methods=["POST"])
def translate():

    data = request.get_json()

    text = data.get("text", "")

    language = data.get("language", "Hindi")

    translated = translate_text(text, language)

    save_history("Translate", translated)

    return jsonify({
        "result": translated
    })


# SUMMARIZE
@app.route("/summarize", methods=["POST"])
def summarize():

    data = request.get_json()

    text = data.get("text", "")

    language = data.get("language", "English")

    summary = summarize_text(text, language)

    save_history("Summary", summary)

    return jsonify({
        "result": summary
    })


# DOWNLOAD PDF
@app.route("/download", methods=["POST"])
def download():

    data = request.get_json()

    content = data.get("content", "")

    filename = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    filepath = os.path.join(
        DOWNLOAD_FOLDER,
        filename
    )

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    for line in content.split("\n"):

        story.append(
            Paragraph(line, styles["BodyText"])
        )

        story.append(Spacer(1, 10))

    doc.build(story)

    return send_file(
        filepath,
        as_attachment=True
    )


# HISTORY SAVE
def save_history(action, content):

    history = []

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []

    history.append({
        "action": action,
        "content": content,
        "time": str(datetime.now())
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# HISTORY GET
@app.route("/history")
def history():

    if not os.path.exists(HISTORY_FILE):
        return jsonify([])

    with open(HISTORY_FILE, "r") as f:

        try:
            data = json.load(f)
        except:
            data = []

    return jsonify(data)


# CLEAR
@app.route("/clear", methods=["POST"])
def clear():

    global current_document

    current_document = ""

    return jsonify({
        "message": "Cleared"
    })


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
