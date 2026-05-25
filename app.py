from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_file
)

from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from deep_translator import GoogleTranslator

import os
import uuid
import datetime
import fitz
import docx

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.pagesizes import letter


# =========================================
# APP CONFIG
# =========================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "super-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["UPLOAD_FOLDER"] = "uploads"

app.config["DOWNLOAD_FOLDER"] = "downloads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)


# =========================================
# LOGIN MANAGER
# =========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# =========================================
# DATABASE MODELS
# =========================================

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))


class History(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    action = db.Column(db.String(100))

    content = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow
    )


# =========================================
# USER LOADER
# =========================================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# =========================================
# TEXT EXTRACTION
# =========================================

def extract_text(filepath):

    ext = filepath.split(".")[-1].lower()

    text = ""

    try:

        # TXT
        if ext == "txt":

            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                text = f.read()

        # PDF
        elif ext == "pdf":

            pdf = fitz.open(filepath)

            for page in pdf:

                text += page.get_text()

        # DOCX
        elif ext == "docx":

            document = docx.Document(filepath)

            for para in document.paragraphs:

                text += para.text + "\n"

        return text.strip()

    except Exception as e:

        return f"Error extracting text: {str(e)}"


# =========================================
# SUMMARY
# =========================================

def generate_summary(text):

    if not text:

        return "No text found"

    sentences = text.split(".")

    summary = ".".join(sentences[:5])

    return summary


# =========================================
# TRANSLATE
# =========================================

def translate_text(text, target_language):

    try:

        translated = GoogleTranslator(
            source='auto',
            target=target_language
        ).translate(text)

        return translated

    except Exception as e:

        return f"Translation Error: {str(e)}"


# =========================================
# PDF CREATOR
# =========================================

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter


def create_pdf(text):

    try:

        filename = f"{uuid.uuid4()}.pdf"

        filepath = os.path.join(
            app.config["DOWNLOAD_FOLDER"],
            filename
        )

     
        # FONT PATH
font_path = "static/fonts/NotoSansDevanagari-Regular.ttf"

print("USING FONT PATH:", font_path)

# CHECK FONT EXISTS
if not os.path.exists(font_path):

    print("FONT FILE NOT FOUND")

    return None

print("FONT FOUND SUCCESSFULLY")

# REGISTER FONT
pdfmetrics.registerFont(
    TTFont(
        "HindiFont",
        font_path
    )
)
        # CREATE CANVAS
        c = canvas.Canvas(
            filepath,
            pagesize=letter
        )

        width, height = letter

        c.setFont(
            "HindiFont",
            14
        )

        y = height - 50

        lines = text.split("\n")

        for line in lines:

            if y < 50:

                c.showPage()

                c.setFont(
                    "HindiFont",
                    14
                )

                y = height - 50

            c.drawString(
                40,
                y,
                str(line)
            )

            y -= 25

        c.save()

        print("PDF SAVED:", filepath)

        return filepath

    except Exception as e:

        print("PDF ERROR:", str(e))

        return None


# =========================================
# HOME
# =========================================

@app.route("/")
@login_required
def home():

    return render_template(
        "index.html",
        username=current_user.username
    )


# =========================================
# SIGNUP
# =========================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if current_user.is_authenticated:

        return redirect(url_for("home"))

    if request.method == "POST":

        username = request.form.get("username")

        email = request.form.get("email")

        password = request.form.get("password")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return render_template(
                "signup.html",
                error="User already exists"
            )

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)

        db.session.commit()

        login_user(new_user)

        return redirect(url_for("home"))

    return render_template("signup.html")


# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        return redirect(url_for("home"))

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid Email or Password"
        )

    return render_template("login.html")


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# =========================================
# UPLOAD
# =========================================

@app.route("/upload", methods=["POST"])
@login_required
def upload():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "No file uploaded"
            })

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "error": "No selected file"
            })

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        extracted_text = extract_text(filepath)

        # SAVE HISTORY
        history = History(
            user_id=current_user.id,
            action=f"Uploaded File: {filename}",
            content=extracted_text[:1000]
        )

        db.session.add(history)

        db.session.commit()

        return jsonify({
            "success": True,
            "text": extracted_text
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================================
# TRANSLATE
# =========================================

@app.route("/translate", methods=["POST"])
@login_required
def translate():

    try:

        data = request.json

        text = data.get("text")

        language = data.get("language")

        translated_text = translate_text(
            text,
            language
        )

        history = History(
            user_id=current_user.id,
            action=f"Translated to {language}",
            content=translated_text
        )

        db.session.add(history)

        db.session.commit()

        return jsonify({
            "result": translated_text
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================================
# SUMMARIZE
# =========================================

@app.route("/summarize", methods=["POST"])
@login_required
def summarize():

    try:

        data = request.json

        text = data.get("text")

        language = data.get("language")

        summary = generate_summary(text)

        if language != "en":

            summary = translate_text(
                summary,
                language
            )

        history = History(
            user_id=current_user.id,
            action=f"Summary ({language})",
            content=summary
        )

        db.session.add(history)

        db.session.commit()

        return jsonify({
            "result": summary
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# =========================================
# DOWNLOAD PDF
# =========================================

@app.route("/download", methods=["POST"])
@login_required
def download():

    try:

        data = request.get_json()

        text = data.get("text", "")

        if not text.strip():

            return jsonify({
                "error": "No text available"
            }), 400

        filepath = create_pdf(text)

        # CHECK PDF CREATED
        if not filepath:

            return jsonify({
                "error": "PDF creation failed"
            }), 500

        # CHECK FILE EXISTS
        if not os.path.exists(filepath):

            return jsonify({
                "error": "PDF file not found"
            }), 500

        return send_file(
            filepath,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="translated_document.pdf"
        )

    except Exception as e:

        print("DOWNLOAD ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500

# =========================================
# HISTORY PAGE
# =========================================

@app.route("/history-page")
@login_required
def history_page():

    records = History.query.filter_by(
        user_id=current_user.id
    ).order_by(
        History.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        records=records
    )


# =========================================
# CLEAR
# =========================================

@app.route("/clear", methods=["POST"])
@login_required
def clear():

    return jsonify({
        "success": True
    })


# =========================================
# CREATE DATABASE
# =========================================

with app.app_context():

    db.create_all()


# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
