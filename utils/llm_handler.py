from deep_translator import GoogleTranslator

# =========================
# SIMPLE SENTENCE SPLITTER
# =========================

def split_sentences(text):
    separators = [".", "!", "?"]

    for sep in separators:
        text = text.replace(sep, sep + "|")

    sentences = text.split("|")

    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) > 5:
            clean_sentences.append(sentence)

    return clean_sentences


# =========================
# SUMMARIZE TEXT
# =========================

def summarize_text(text, language="English"):

    try:

        if not text.strip():
            return "No text found."

        # Clean text
        text = text.replace("\n", " ").strip()

        # Split into sentences
        sentences = split_sentences(text)

        if len(sentences) == 0:
            return "Unable to summarize."

        # Take first important sentences
        summary_sentences = sentences[:5]

        summary = ". ".join(summary_sentences)

        if not summary.endswith("."):
            summary += "."

        # Translate summary if needed
        if language != "English":

            lang_map = {
                "Hindi": "hi",
                "French": "fr",
                "German": "de",
                "Spanish": "es",
                "Japanese": "ja",
                "Korean": "ko",
                "Russian": "ru",
                "Arabic": "ar",
                "Chinese": "zh-CN"
            }

            target_lang = lang_map.get(language)

            if target_lang:

                summary = GoogleTranslator(
                    source='auto',
                    target=target_lang
                ).translate(summary)

        return summary

    except Exception as e:
        return f"Summary Error: {str(e)}"


# =========================
# TRANSLATE TEXT
# =========================

def translate_text(text, language):

    try:

        if not text.strip():
            return "No text found."

        lang_map = {
            "Hindi": "hi",
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Japanese": "ja",
            "Korean": "ko",
            "Russian": "ru",
            "Arabic": "ar",
            "Chinese": "zh-CN"
        }

        target_lang = lang_map.get(language)

        if not target_lang:
            return text

        translated = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(text)

        return translated

    except Exception as e:
        return f"Translation Error: {str(e)}"


# =========================
# CHAT WITH DOCUMENT
# =========================

def answer_question(context, question):

    try:

        context = context.lower()
        question = question.lower()

        sentences = split_sentences(context)

        best_sentence = ""

        for sentence in sentences:

            if any(word in sentence for word in question.split()):
                best_sentence = sentence
                break

        if best_sentence:
            return best_sentence

        return "Answer not found in document."

    except Exception as e:
        return f"Chat Error: {str(e)}"
