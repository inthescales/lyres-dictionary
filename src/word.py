from enum import Enum
from typing import Optional

from src.env import Env
from src.morph import Morph
from src.morph_view import Element, MorphView

class WordType(Enum):
    """The type (aka 'lexical category' or 'part of speech') of a word"""
    noun = 0
    adjective = 1
    verb = 2
    adverb = 3

    @property
    def string(self) -> str:
        """A string representation of the type, as it should appear in entries"""
        match self:
            case WordType.noun:
                return "noun"
            case WordType.adjective:
                return "adj"
            case WordType.verb:
                return "verb"
            case WordType.adverb:
                return "adv"

# A word
class Word:
    """Representation of a word as a sequence of elements."""

    def __init__(self, elements: Optional[list[Element]] = None):
        if elements is None:
            elements = []

        self._elements: list[Element] = elements

    def set_morphs(self, morphs: list[Morph]) -> None:
        """Assigns the word's element list to one built from the given morphs."""
        for i in range(0, len(morphs)):
            env: Env = Env(
                prev=morphs[i - 1] if i > 0 else None,
                next=morphs[i + 1] if i < len(morphs) - 1 else None
            )
            self._elements.append(MorphView(morph=morphs[i], env=env))

    @property
    def form(self) -> str:
        """The word's form as a string"""
        f: str = ""
        for element in self._elements:
            f += element.form

        return f

    @property
    def type(self) -> WordType:
        """The type of the word"""
        return WordType.noun

    @property
    def definition(self) -> str:
        """The word's definition as a string"""
        return "definition"
