import os
from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)

translator = Translator()

uploaded_text = ""

@app.route("/")
def home():

    return render_template("index.html")

# Upload Route
@app.route("/upload", methods=["POST"])
def upload():

    global uploaded_text

    file = request.files["file"]

    uploaded_text = file.read().decode("utf-8")

    return jsonify({
        "message":"Document uploaded successfully!"
    })

# Summarize Route
@app.route("/summarize")
def summarize():

    global uploaded_text

    if uploaded_text == "":

        return jsonify({
            "summary":"No document uploaded."
        })

    summary = uploaded_text[:500]

    return jsonify({
        "summary":summary
    })

# Translate Route
@app.route("/translate", methods=["POST"])
def translate():

    data = request.get_json()

    text = data["text"]

    target = data["target"]

    translated = translator.translate(text, dest=target)

    return jsonify({
        "translated_text":translated.text
    })

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port, debug=False)