from googletrans import Translator

translator = Translator()

def translate_text(text):

    translated = translator.translate(
        text,
        dest="hi"
    )

    return translated.text