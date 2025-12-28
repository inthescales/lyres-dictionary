from enum import Enum
from typing import Self

from word_base.element.classes.element_class import ElementClass

class WordClassException(Exception):
    """Exception to be raised if a word would be generated with an invalid lexical class."""
    def __init__(self, element_class: ElementClass):
        self.args = (["Invalid final element type '" + str(element_class) + "' for word"], element_class)

class WordClass(Enum):
    """The lexical class(a.k.a. 'part of speech') of a word"""
    noun = 0
    adjective = 1
    verb = 2
    adverb = 3

    @property
    def string(self) -> str:
        """A string representation of the type, as it should appear in entries"""
        match self:
            case WordClass.noun:
                return "noun"
            case WordClass.adjective:
                return "adj"
            case WordClass.verb:
                return "verb"
            case WordClass.adverb:
                return "adv"

    @classmethod
    def from_element_type(cls, final_element_type: ElementClass) -> Self:
        match final_element_type:
            case ElementClass.noun | ElementClass.number:
                return WordClass.noun
            case ElementClass.adjective:
                return WordClass.adjective
            case ElementClass.verb:
                return WordClass.verb
            case ElementClass.derive | ElementClass.inflect:
                raise WordClassException(final_element_type)
