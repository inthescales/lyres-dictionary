from abc import ABC, abstractmethod

from src.elements.element import Element
from src.senses.sense import Sense
from src.types.element_type import ElementType, TypeData

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
    def type_data(self) -> TypeData:
        """A type data object indicating this element's type along with any related data."""
        pass

    @property
    def type(self) -> ElementType:
        """The lexical category that this element gives to the word."""
        return self.type_data.type