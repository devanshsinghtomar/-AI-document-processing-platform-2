
from transformers import pipeline


# LOAD SUMMARIZER MODEL

summarizer = pipeline(

    task="summarization",

    model="facebook/bart-large-cnn"
)


def summarize_text(text):

    # LIMIT VERY LARGE TEXT

    text = text[:2000]

    result = summarizer(

        text,

        max_length=120,

        min_length=30,

        do_sample=False
    )

    return result[0]["summary_text"] 
