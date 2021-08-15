from enum import Enum

class Language(Enum):
    ENG = ('English', 'en-US')
    JP = ('Japanese', 'ja-JP')

    def get_code(_lang):
        if _lang == Language.ENG.value[0]:
            return Language.ENG.value[1]
        
        if _lang == Language.JP.value[0]:
            return Language.JP.value[1]
    