import fitz


def extract_text_from_file(filepath):

    text=""

    if filepath.endswith(".pdf"):

        pdf=fitz.open(filepath)

        for page in pdf:
            text+=page.get_text()

    elif filepath.endswith(".txt"):

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            text=f.read()

    return text 
