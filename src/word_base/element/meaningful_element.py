from abc import ABC, abstractmethod

from word_base.element.element import Element
from word_base.senses.sense import Sense
from word_base.lex_class.lex_class import LexClass, ClassData

class MeaningfulElement(Element, ABC):
    """An element that contributes to the meaning of a word"""
    @property
    @abstractmethod
    def sense(self) -> Sense:
        """The sense carried by this element."""
        pass

    @property
    def gloss(self) -> str:
        """The gloss text for this element's sense in context."""
        return self.sense.gloss_provider.gloss(self.env)

    @property
    @abstractmethod
    def class_data(self) -> ClassData:
        """A type data object indicating this element's type along with any related data."""
        pass

    @property
    def lex_class(self) -> LexClass:
        """The lexical category that this element gives to the word."""
        return self.class_data.lex_class