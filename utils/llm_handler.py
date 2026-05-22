from googletrans import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

translator = Translator()

LANGUAGE_CODES = {
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


def translate_text(text, language):

    try:

        if language == "English":
            return text

        lang_code = LANGUAGE_CODES.get(language, "en")

        translated = translator.translate(
            text,
            dest=lang_code
        )

        return translated.text

    except Exception as e:

        return f"Translation Error: {str(e)}"


def summarize_text(text, language="English"):

    try:

        # STEP 1:
        # Translate FULL document first

        if language != "English":

            translated_full_text = translate_text(
                text,
                language
            )

            working_text = translated_full_text

        else:

            working_text = text

        # STEP 2:
        # Create summary from translated text

        parser = PlaintextParser.from_string(
            working_text,
            Tokenizer("english")
        )

        summarizer = LsaSummarizer()

        summary_sentences = summarizer(
            parser.document,
            5
        )

        summary = " ".join(
            [str(sentence) for sentence in summary_sentences]
        )

        return summary

    except Exception as e:

        return f"Summary Error: {str(e)}"
