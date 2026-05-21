import re

def extract_data(text):

    emails = re.findall(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text
    )

    phones = re.findall(

        r"\d{10}",

        text
    )

    return {

        "emails": emails,

        "phones": phones
    }