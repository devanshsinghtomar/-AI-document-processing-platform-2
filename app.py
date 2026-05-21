from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==========================================
# CLOUDINARY CONFIG
# ==========================================

cloudinary.config(
    cloud_name="dityosbba",
    api_key="645318632592627",
    api_secret="YOUR_CLOUDINARY_SECRET"
)

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return "AI Document Platform Running"

# ==========================================
# UPLOAD
# ==========================================

@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:

            return jsonify({
                "success": False,
                "message": "No file uploaded"
            })

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "message": "No selected file"
            })

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        # Upload to Cloudinary

        upload_result = cloudinary.uploader.upload(
            filepath,
            resource_type="auto"
        )

        file_url = upload_result["secure_url"]

        extracted_text = ""

        # PDF Extraction

        if filename.lower().endswith(".pdf"):

            pdf_reader = PdfReader(filepath)

            for page in pdf_reader.pages:

                text = page.extract_text()

                if text:
                    extracted_text += text + "\n"

        return jsonify({
            "success": True,
            "url": file_url,
            "text": extracted_text,
            "filename": filename
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

# ==========================================
# TRANSLATE
# ==========================================

@app.route("/translate", methods=["POST"])
def translate():

    try:

        data = request.json

        text = data.get("text")

        translated = "Translated Version:\n\n" + text

        return jsonify({
            "success": True,
            "translated_text": translated
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

# ==========================================
# SUMMARIZE
# ==========================================

@app.route("/summarize", methods=["POST"])
def summarize():

    try:

        data = request.json

        text = data.get("text")

        summary = text[:500]

        return jsonify({
            "success": True,
            "summary": summary
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
