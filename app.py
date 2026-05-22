from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================

app.config['SECRET_KEY'] = os.environ.get(
    "SECRET_KEY",
    "super-secret-key"
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# =========================
# LOGIN MANAGER
# =========================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# =========================
# DATABASE MODEL
# =========================

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# =========================
# USER LOADER
# =========================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================
# HOME
# =========================

@app.route('/')
@login_required
def home():
    return render_template('index.html')

# =========================
# SIGNUP
# =========================

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "User already exists"

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for('home'))

    return render_template('signup.html')

# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for('home'))

        return "Invalid credentials"

    return render_template('login.html')

# =========================
# LOGOUT
# =========================

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# =========================
# UPLOAD
# =========================

@app.route('/upload', methods=['POST'])
@login_required
def upload():

    if 'file' not in request.files:
        return jsonify({
            'error': 'No file uploaded'
        })

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'error': 'No selected file'
        })

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    file.save(filepath)

    return jsonify({
        'success': True,
        'filename': filename
    })

# =========================
# SUMMARIZE
# =========================

@app.route('/summarize', methods=['POST'])
@login_required
def summarize():

    text = request.json.get('text')

    if not text:
        return jsonify({
            'result': 'No text found'
        })

    summary = text[:300] + "..."

    return jsonify({
        'result': summary
    })

# =========================
# TRANSLATE
# =========================

@app.route('/translate', methods=['POST'])
@login_required
def translate():

    text = request.json.get('text')

    translated = "Translated: " + text

    return jsonify({
        'result': translated
    })

# =========================
# CHAT
# =========================

@app.route('/chat', methods=['POST'])
@login_required
def chat():

    message = request.json.get('message')

    response = f"AI Response: {message}"

    return jsonify({
        'result': response
    })

# =========================
# CONVERT
# =========================

@app.route('/convert', methods=['POST'])
@login_required
def convert():

    return jsonify({
        'result': 'Document converted successfully'
    })

# =========================
# CREATE DB
# =========================

with app.app_context():
    db.create_all()

# =========================
# RUN
# =========================

if __name__ == '__main__':
    app.run(debug=True)
