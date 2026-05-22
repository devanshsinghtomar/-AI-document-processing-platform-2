from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    session
)

from werkzeug.utils import secure_filename

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from functools import wraps

import os
import json

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from utils.document_processor import extract_text_from_file

from utils.llm_handler import (
    translate_text,
    summarize_text,
)

# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

# =========================================================
# SECRET KEY
# =========================================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "super-secret-key-change-this"
)

# =========================================================
# SESSION SECURITY
# =========================================================

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# =========================================================
# FOLDERS
# =========================================================

UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
HISTORY_FILE = "history/history.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs("history", exist_ok=True)

current_document = ""

# =========================================================
# USER DATABASE
# =========================================================
# Change credentials if needed

users = {
    "admin": generate_password_hash("admin123")
}

# =========================================================
# LOGIN REQUIRED DECORATOR
# =========================================================

def login_required(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        if "user" not in session:

            return jsonify({
                "success": False,
                "error": "Unauthorized access. Please login."
            }), 401

        return f(*args, **kwargs)

    return decorated_function

# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")

# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template("login.html")

    try:

        data = request.get_json()

        username = data.get(
            "username",
            ""
        ).strip()

        password = data.get(
            "password",
            ""
        ).strip()

        # Empty validation
        if not username or not password:

            return jsonify({
                "success": False,
                "error": "Username and password required"
            }), 400

        # Check user
        if username in users:

            if check_password_hash(
                users[username],
                password
            ):

                session["user"] = username

                return jsonify({
                    "success": True,
                    "message": "Login successful"
                })

        return jsonify({
            "success": False,
            "error": "Invalid username or password"
        }), 401

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })

# =========================================================
# CHECK AUTH
# =========================================================

@app.route("/check-auth")
def check_auth():

    if "user" in session:

        return jsonify({
            "authenticated": True,
            "user": session["user"]
        })

    return jsonify({
        "authenticated": False
    })

# =========================================================
# UPLOAD
# =========================================================

@app.route("/upload", methods=["POST"])
@login_required
def upload():

    global current_document

    try:

        if "file" not in request.files:

            return jsonify({
                "success": False,
                "error": "No file uploaded"
            })

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "error": "Empty filename"
            })

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        current_document = extract_text_from_file(
            filepath
        )

        return jsonify({
            "success": True,
            "text": current_document
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# =========================================================
# TRANSLATE
# =========================================================

@app.route("/translate", methods=["POST"])
@login_required
def translate():

    try:

        data = request.get_json()

        text = data.get(
            "text",
            ""
        ).strip()

        language = data.get(
            "language",
            "Hindi"
        )

        if not text:

            return jsonify({
                "success": False,
                "error": "Text is required"
            })

        translated = translate_text(
            text,
            language
        )

        save_history(
            "Translate",
            translated
        )

        return jsonify({
            "success": True,
            "result": translated
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# =========================================================
# SUMMARIZE
# =========================================================

@app.route("/summarize", methods=["POST"])
@login_required
def summarize():

    try:

        data = request.get_json()

        text = data.get(
            "text",
            ""
        ).strip()

        language = data.get(
            "language",
            "English"
        )

        if not text:

            return jsonify({
                "success": False,
                "error": "Text is required"
            })

        summary = summarize_text(
            text,
            language
        )

        save_history(
            "Summary",
            summary
        )

        return jsonify({
            "success": True,
            "result": summary
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# =========================================================
# DOWNLOAD PDF
# =========================================================

@app.route("/download", methods=["POST"])
@login_required
def download():

    try:

        data = request.get_json()

        content = data.get(
            "content",
            ""
        )

        if not content:

            return jsonify({
                "success": False,
                "error": "No content provided"
            })

        filename = (
            f"output_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        )

        filepath = os.path.join(
            DOWNLOAD_FOLDER,
            filename
        )

        doc = SimpleDocTemplate(
            filepath
        )

        styles = getSampleStyleSheet()

        story = []

        for line in content.split("\n"):

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 10)
            )

        doc.build(story)

        return send_file(
            filepath,
            as_attachment=True
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# =========================================================
# SAVE HISTORY
# =========================================================

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

        json.dump(
            history,
            f,
            indent=4
        )

# =========================================================
# GET HISTORY
# =========================================================

@app.route("/history")
@login_required
def history():

    if not os.path.exists(HISTORY_FILE):

        return jsonify([])

    with open(HISTORY_FILE, "r") as f:

        try:

            data = json.load(f)

        except:

            data = []

    return jsonify(data)

# =========================================================
# CLEAR
# =========================================================

@app.route("/clear", methods=["POST"])
@login_required
def clear():

    global current_document

    current_document = ""

    return jsonify({
        "success": True,
        "message": "Cleared"
    })

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
