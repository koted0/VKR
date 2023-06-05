from spellchecker import SpellChecker


class CorrectOCR:
    @classmethod
    def check_spelling(cls, text: str):
        corrected_words = []
        spell_checker = SpellChecker()
        for word in text.split():
            if not word.isalpha():
                corrected_words.append(word)
            else:
                corrected_word = spell_checker.correction(word)
                if corrected_word is not None:
                    corrected_words.append(corrected_word)
                else:
                    corrected_words.append(word)
        return ' '.join(corrected_words)

    # @classmethod
    # # in development
    # def check_grammar(cls, text):
    #     tool = language_tool_python.LanguageTool('en-US')
    #     matches = tool.check(text)
    #     corrected_text = language_tool_python.utils.correct(text, matches)
    #     return corrected_text
