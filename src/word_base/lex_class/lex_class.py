from enum import auto, StrEnum

class LexClass(StrEnum):
    noun      = auto()
    adjective = auto()
    verb      = auto()
    number    = auto()
    derive    = auto()

    @property
    def is_root(self) -> bool:
        match self:
            case LexClass.noun, LexClass.adjective, LexClass.verb, LexClass.number:
                return True
            case LexClass.derive:
                return False

class ClassData:
    def __init__(self, morph_class: LexClass):
        self.lex_class = morph_class

class DeriveClassData(ClassData):
    def __init__(self, result_data: ClassData):
        ClassData.__init__(self, LexClass.derive)
        self.result_data = result_data
