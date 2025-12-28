from abc import ABC, abstractmethod

from word_base.element.classes.element_class import ElementClass, ClassData

# This class is separated out from the Element class in order to prevent a circular import between Element and Env.

class ElementBase(ABC):
    """Base data belonging to all elements."""

    @property
    @abstractmethod
    def form(self) -> str:
        pass

    @property
    @abstractmethod
    def class_data(self) -> ClassData:
        """A type data object indicating this element's type along with any related data."""
        pass

    @property
    def lex_class(self) -> ElementClass:
        """The lexical category that this element gives to the word."""
        return self.class_data.lex_class
