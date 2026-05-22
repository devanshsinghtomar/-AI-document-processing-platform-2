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

        parser = PlaintextParser.from_string(
            text,
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

        if language != "English":
            summary = translate_text(summary, language)

        return summary

    except Exception as e:

        return f"Summary Error: {str(e)}"


def answer_question(context, question):

    context = context.lower()

    question = question.lower()

    if question in context:
        return "Answer found in document."

    return "This lightweight version supports basic document searching only."
