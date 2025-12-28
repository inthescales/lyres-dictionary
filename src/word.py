from enum import Enum
from typing import Optional, Self

import glosses as gloss
from word_base.element.element import Element
from word_base.element.meaningful_element import MeaningfulElement
from word_base.lex_class.lex_class import LexClass, DeriveClassData

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

    @classmethod
    def from_element_type(cls, final_element_type: LexClass) -> Self:
        match final_element_type:
            case LexClass.noun:
                return WordType.noun
            case LexClass.adjective:
                return WordType.adjective
            case LexClass.verb:
                return WordType.verb
            case LexClass.number:
                return WordType.noun
            case LexClass.derive:
                # TODO: Fill this in
                raise Exception()

# A word
class Word:
    """Representation of a word as a sequence of element."""

    def __init__(self, root: Element):
        self._form_elements: list[Element] = [root]
        self._meaning_elements: list[MeaningfulElement] = []
        if isinstance(root, MeaningfulElement):
            self._meaning_elements = [root]


    def add_prefix(self, prefix: Element):
        prefix.env.next = self.head_element
        self.head_element.env.prev = prefix
        self._form_elements = [prefix] + self._form_elements

        if isinstance(prefix, MeaningfulElement):
            self._meaning_elements.append(prefix)

    def add_suffix(self, suffix: Element):
        suffix.env.prev = self.tail_element
        self.tail_element.env.next = suffix
        self._form_elements.append(suffix)

        if isinstance(suffix, MeaningfulElement):
            self._meaning_elements.append(suffix)

    @property
    def form(self) -> str:
        """The word's form as a string"""
        f: str = ""
        for element in self._form_elements:
            f += element.form

        return f

    @property
    def type(self) -> WordType:
        """The type of the word"""

        e_type: LexClass = self._meaning_elements[0].lex_class
        for element in self._meaning_elements[1:]:
            if element.lex_class == LexClass.derive and isinstance(element.class_data, DeriveClassData):
                e_type = element.class_data.result_data.lex_class
            else:
                # TODO: Fill this in
                raise Exception

        return WordType.from_element_type(e_type)

    @property
    def definition(self) -> str:
        """The word's definition as a string"""
        definition: str = self._meaning_elements[0].gloss
        prev_element: MeaningfulElement = self._meaning_elements[0]
        for element in self._meaning_elements[1:]:
            definition = gloss.substitute(prev_element.sense, element.gloss, definition)
            prev_element = element

        return definition

    @property
    def head_element(self) -> Optional[Element]:
        return self._form_elements[0]

    @property
    def tail_element(self) -> Optional[Element]:
        return self._form_elements[-1]
