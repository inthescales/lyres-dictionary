from enum import StrEnum

class ElementClass(StrEnum):
    noun      = "noun"
    adjective = "adjective"
    verb      = "verb"
    number    = "number"
    derive    = "derive"
    inflect   = "inflect"

    @property
    def is_root(self) -> bool:
        """Whether this type is a root type."""
        match self:
            case ElementClass.noun | ElementClass.adjective | ElementClass.verb | ElementClass.number:
                return True
            case ElementClass.derive | ElementClass.inflect:
                return False

class ClassData:
    """Base type containing any additional data necessary for words of a given lexical class in a given language."""
    def __init__(self, morph_class: ElementClass):
        self.lex_class = morph_class
