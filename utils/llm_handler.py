from googletrans import Translator
import re

translator = Translator()


# =========================================
# TRANSLATE TEXT
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
# SUMMARIZE TEXT
# =========================================

def summarize_text(text, language="English"):

    try:

        if not text.strip():

            return "No text found."

        # Clean text
        text = re.sub(r'\s+', ' ', text)

        # Split into sentences
        sentences = re.split(r'(?<=[.!?]) +', text)

        # Simple lightweight summary
        summary_sentences = sentences[:5]

        summary = " ".join(summary_sentences)

        # Translate summary if needed
        if language != "English":

            summary = translate_text(
                summary,
                language
            )

        return summary

    except Exception as e:

        return f"Summary Error: {str(e)}"


# =========================================
# QUESTION ANSWERING
# =========================================

def answer_question(context, question):

    try:

        context_lower = context.lower()
        question_lower = question.lower()

        # Very lightweight QA
        sentences = re.split(r'(?<=[.!?]) +', context)

        matching_sentences = []

        for sentence in sentences:

            words = question_lower.split()

            for word in words:

                if word in sentence.lower():

                    matching_sentences.append(sentence)

                    break

        if matching_sentences:

            return " ".join(matching_sentences[:3])

        return "Answer not found in document."

    except Exception as e:

        return f"Chat Error: {str(e)}"
