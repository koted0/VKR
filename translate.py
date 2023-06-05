from deep_translator import GoogleTranslator

def translate_text(text, source_lang='en', target_lang='ru'):
    translators = GoogleTranslator(source=source_lang, target=target_lang)
    return translators.translate(text)
