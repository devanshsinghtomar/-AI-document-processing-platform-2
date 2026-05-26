from transformers import pipeline
import re

# Load model once when server starts
humanizer_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)

# Prompt template
PROMPT = """
Rewrite the following text in a natural, human-like, engaging, and readable style.
Keep the original meaning exactly same.
Do not add extra information.
Do not remove important information.
Make the writing feel less robotic and more human.

Text:
"""

def clean_text(text):
    """
    Clean extra spaces and formatting
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_text(text, max_words=200):
    """
    Split long text into smaller chunks
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks


def humanize_chunk(chunk):
    """
    Humanize one chunk
    """
    prompt = PROMPT + chunk

    result = humanizer_pipeline(
        prompt,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.8,
        top_p=0.95
    )

    return result[0]["generated_text"]


def humanize_text(text):
    """
    Main function for humanizing text
    """
    try:
        text = clean_text(text)

        if not text:
            return "Please enter some text."

        chunks = split_text(text)

        humanized_chunks = []

        for chunk in chunks:
            humanized = humanize_chunk(chunk)
            humanized_chunks.append(humanized)

        final_output = "\n\n".join(humanized_chunks)

        return final_output

    except Exception as e:
        return f"Error while humanizing text: {str(e)}"
