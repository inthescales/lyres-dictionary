from abc import ABC, abstractmethod

from src.elements.element import Element
from src.senses.sense import Sense

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
