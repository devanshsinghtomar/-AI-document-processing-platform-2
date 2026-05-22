from googletrans import Translator
import re

translator = Translator()


# =========================================
# TRANSLATION
# =========================================

def translate_text(text, language):

    try:

        language_codes = {
            "Hindi": "hi",
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Japanese": "ja",
            "Korean": "ko",
            "Russian": "ru",
            "Arabic": "ar",
            "Chinese": "zh-cn",
            "English": "en"
        }

        lang_code = language_codes.get(language, "en")

        translated = translator.translate(
            text,
            dest=lang_code
        )

        return translated.text

    except Exception as e:

        return f"Translation Error: {str(e)}"


# =========================================
# SUMMARY
# =========================================

def summarize_text(text, language="English"):

    try:

        if not text.strip():

            return "No text found."

        text = re.sub(r'\s+', ' ', text)

        sentences = re.split(r'(?<=[.!?]) +', text)

        summary = " ".join(sentences[:5])

        if language != "English":

            summary = translate_text(
                summary,
                language
            )

        return summary

    except Exception as e:

        return f"Summary Error: {str(e)}"


# =========================================
# CHAT
# =========================================

def answer_question(context, question):

    try:

        context_sentences = re.split(
            r'(?<=[.!?]) +',
            context
        )

        question_words = question.lower().split()

        matched = []

        for sentence in context_sentences:

            for word in question_words:

                if word in sentence.lower():

                    matched.append(sentence)

                    break

        if matched:

            return " ".join(matched[:3])

        return "Answer not found."

    except Exception as e:

        return f"Chat Error: {str(e)}"
