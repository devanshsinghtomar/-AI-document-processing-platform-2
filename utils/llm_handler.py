# ==========================================
# LIGHTWEIGHT AI FUNCTIONS
# ==========================================

def summarize_text(text, language="English"):

    if len(text.strip()) == 0:
        return "No text found."

    # Simple summary
    sentences = text.split(".")

    summary = ".".join(sentences[:5])

    return summary + "."


# ==========================================
# TRANSLATION
# ==========================================

def translate_text(text, language):

    # Dummy lightweight translation

    return f"[Translated to {language}]\n\n{text}"


# ==========================================
# QUESTION ANSWERING
# ==========================================

def answer_question(context, question):

    context = context[:1000]

    # Simple keyword response

    if question.lower() in context.lower():

        return "Answer found in document."

    return context[:300]
