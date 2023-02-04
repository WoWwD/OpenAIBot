from deep_translator import GoogleTranslator


class TranslatorApi:
    def toLanguage(self, text, language):
        return GoogleTranslator(source='auto', target=language).translate(text)
