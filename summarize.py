from transformers import pipeline

summarizer = pipeline(
    "text-generation",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarize_text(text):

    text = text[:1000]

    prompt = f"Summarize this:\n{text}"

    result = summarizer(
        prompt,
        max_new_tokens=120,
        do_sample=False
    )

    return result[0]["generated_text"]
