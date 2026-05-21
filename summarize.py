def summarize_text(text):

    # Simple lightweight summarizer

    text = text.strip()

    if len(text) <= 500:
        return text

    sentences = text.split(".")

    summary = ".".join(sentences[:5])

    return summary + "."
