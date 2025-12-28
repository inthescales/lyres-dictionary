from abc import ABC
from enum import StrEnum

class ElementClass(StrEnum):
    noun      = "noun"
    adjective = "adjective"
    verb      = "verb"
    number    = "number"
    derive    = "derive"

    @property
    def is_root(self) -> bool:
        """Whether this type is a root type."""
        match self:
            case ElementClass.noun, ElementClass.adjective, ElementClass.verb, ElementClass.number:
                return True
            case ElementClass.derive:
                return False

class ClassData(ABC):
    """Base type containing any additional element related to a lexical class in a given language."""
    def __init__(self, morph_class: ElementClass):
        self.lex_class = morph_class

class DeriveClassData(ClassData):
    """Base type for derivational elements."""
    def __init__(self, result_data: ClassData):
        ClassData.__init__(self, ElementClass.derive)
        self.result_data = result_data
