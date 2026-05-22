from transformers import pipeline
from deep_translator import GoogleTranslator

# SMALL MODELS FOR LOW RAM

summarizer = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)

qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)


def translate_text(text, language):

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

    if language == "English":
        return text

    try:

        translated = GoogleTranslator(
            source='auto',
            target=lang_map[language]
        ).translate(text)

        return translated

    except Exception as e:

        return f"Translation Error: {str(e)}"


def summarize_text(text, language="English"):

    if len(text.strip()) == 0:
        return "No text found."

    text = text[:1500]

    try:

        result = summarizer(
            f"summarize: {text}",
            max_length=120,
            min_length=40
        )

        summary = result[0]["generated_text"]

        if language != "English":
            summary = translate_text(summary, language)

        return summary

    except Exception as e:

        return f"Summarization Error: {str(e)}"


def answer_question(context, question):

    try:

        context = context[:1500]

        result = qa_pipeline(
            question=question,
            context=context
        )

        return result["answer"]

    except Exception as e:

        return f"Chat Error: {str(e)}"
