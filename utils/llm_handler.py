from transformers import pipeline

# Summarization model
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

# Question answering model
qa_pipeline = pipeline(
    "question-answering"
)

# Translation models
translator_hi = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-en-hi"
)

translator_fr = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-en-fr"
)

translator_de = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-en-de"
)

translator_es = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-en-es"
)


def summarize_text(text, language="English"):

    if len(text.strip()) == 0:
        return "No text found in document."

    # limit text size
    text = text[:2000]

    try:

        result = summarizer(
            text,
            max_length=120,
            min_length=40,
            do_sample=False
        )

        summary = result[0]["summary_text"]

        # translate summary if language not English
        if language != "English":
            summary = translate_text(summary, language)

        return summary

    except Exception as e:
        return f"Summarization Error: {str(e)}"


def translate_text(text, language):

    text = text[:1500]

    try:

        if language == "Hindi":

            result = translator_hi(text)

        elif language == "French":

            result = translator_fr(text)

        elif language == "German":

            result = translator_de(text)

        elif language == "Spanish":

            result = translator_es(text)

        else:
            return text

        return result[0]["translation_text"]

    except Exception as e:

        return f"Translation Error: {str(e)}"


def answer_question(context, question):

    try:

        context = context[:2000]

        result = qa_pipeline(
            question=question,
            context=context
        )

        return result["answer"]

    except Exception as e:

        return f"Chat Error: {str(e)}" 
